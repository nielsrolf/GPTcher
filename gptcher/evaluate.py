import os

import Levenshtein
import openai
from dotenv import load_dotenv
from unidecode import unidecode

from gptcher.utils import complete_and_parse_json
from gptcher.content.voice_to_text import transcribe

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


template = """In this task, you evaluate students. The students write messages in imperfect <language> or English or a mixture of both. You translate this to perfect English, and perfect <language>, and then list the vocabulary used. If the student seems to be asking for help with using the bot -e.g. asking how to get back to the chat or how to exit this session, also note this. Your response is in JSON with the format used in the example.

Example:
Spanish Student: Hola yo developing un feature nueve para bot: un vocabulary trainer
Output:
{
    "learning_language": "Spanish",
    "msg_english": "Hi, I am developing a new feature for this bot: a vocabulary trainer.",
    "msg_original": "Hola yo developing un feature nueve para bot: un vocabulary trainer",
    "msg_correct": "Hola, estoy desarrollando una nueva función para este bot: un entrenador de vocabulario.",
    "is_asking_for_help": false,
    "vocabulary": [
        {"en": "Hi", "target": "Hola", "student": "Hola"},
        {"en": "I am developing", "target": "estoy desarrollando", "student": "developing"},
        {"en": "a feature", "target": "una función", "student": "un feature"},
        {"en": "nueve", "target": "nueva", "student": "nueve"},
        {"en": "for", "target": "para", "student": "para"},
        {"en": "this bot", "target": "este bot", "student": "bot"}
    ]
}

<language> Student: <message>
Output:
"""

eval_prefix = '''{
    "learning_language": "<language>",
    "msg_english": "'''


eval_prefix_with_english = '''{
    "learning_language": "<language>",
    "msg_english": "<message_en>",'''


# @measure_time
async def evaluate(message, vocabulary, on_fail=None):
    if message.voice_url is not None and message.text is None:
        message.text = transcribe(message.voice_url, vocabulary.language)
    # try:
    if True:
        prompt = template.replace("<message>", message.text).replace("<language>", vocabulary.language)
        if message.text_en is not None:
            prefix = eval_prefix_with_english.replace("<message_en>", message.text_en)
        else:
            prefix = eval_prefix
        prefix = prefix.replace("<language>", vocabulary.language)
        eval_response = complete_and_parse_json(prompt, "\n\n", prefix, max_tokens=1000)
        if eval_response['is_asking_for_help']:
            await vocabulary.user.reply("You can always get help by typing /help")
        message.evaluation = eval_response
        message.to_db()
        total_score = 0
        for wordpair in eval_response["vocabulary"]:
            score = get_score(wordpair["target"], wordpair["student"])
            total_score += score
            if wordpair["en"] not in vocabulary:
                vocabulary.add_wordpair(wordpair["en"], wordpair["target"])
            vocabulary[wordpair["en"]].register_score(score, wordpair["target"])
        vocabulary.to_db()
        if message.text_translated is not None and not almost_equal(message.text, message.text_translated) and on_fail is not None:
            await on_fail()
    # except Exception as e:
    #     print(e)
    #     print("Error in evaluation", message.__dict__)


def normalize_string(s):
    # Replace special characters and remove non-ASCII characters
    s = unidecode(s)
    # Remove any remaining non-alphanumeric characters
    s = "".join(c for c in s if c.isalnum() or c == " ")
    return s.lower().strip()


def almost_equal(s1, s2):
    # Calculate the Levenshtein distance between the two strings
    distance = Levenshtein.distance(normalize_string(s1), normalize_string(s2))
    # Return True if the distance is at most 1, False otherwise
    return distance <= 1


def get_score(translation, original):
    if normalize_string(translation) == normalize_string(original):
        score = 2
    elif almost_equal(translation, original):
        score = 1
    else:
        score = 0
    print("Score:", score, translation, original)
    return score
