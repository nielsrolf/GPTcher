import os

import Levenshtein
import openai
from dotenv import load_dotenv
from unidecode import unidecode

from gptcher.utils import complete

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


template = """In this task, you evaluate a <language> student. The student writes a message in imperfect Spanish or English or a mixture of both. You translate this to perfect English, and perfect Spanish, and then list the vocabulary used.

Example (Spanish):
>> Original: Hola yo developing un feature nueve para eso bot: un vocabulary trainer
>> English:  Hi, I am developing a new feature for this bot: a vocabulary trainer.
>> Translated: Hola, estoy desarrollando una nueva función para este bot: un entrenador de vocabulario.
>> Vocabulary:
- Hi - Hola - Hola
- I am developing - estoy desarrollando - yo developing
- a feature - una función - un feature
- new - nueva - nueve
- for - para - para
- this - este - eso
- bot - bot - bot
- vocabulary - vocabulario - vocabulary
- a trainer - un entrenador - un trainer

Example (<language>):
>> Original: {}
>> English:""".format


# @measure_time
async def evaluate(message, vocabulary):
    response = None
    try:
        prompt = template(message.text).replace("<language>", vocabulary.language)
        # TODO: transcribe if message.text is None and message.voice is not None
        prefix = ""
        if message.text_en is not None:
            prefix = " " + message.text_en + "\n>> Translated:"
            prompt += prefix
            if message.text_translated is not None:
                prefix += message.text_translated + "\n>> Vocabulary:"

        response = complete(prompt, stop=["\n\n", ">> Original:"])
        print(prompt + response)
        response = prefix + response
        # Extract Enflish and Translated
        english = response.split("\n>> Translated:")[0].strip()
        translated, word_scores = response.split("\n>> Translated:")[1].split(
            "\n>> Vocabulary"
        )
        translated = translated.strip()
        word_scores = word_scores.strip()
        if not word_scores.startswith("-"):
            word_scores = "-" + word_scores
        for pair in word_scores.split("\n"):
            if pair == "":
                continue
            try:
                _, word_en, translation, original = pair.split("-")
            except ValueError:
                print("Unparseable gpt response:", pair)
                continue
            score = get_score(translation, original)
            word_en = word_en.strip()
            translation = translation.strip()
            if word_en not in vocabulary:
                vocabulary.add_wordpair(word_en, translation)
            vocabulary[word_en].register_score(score, translation)
        vocabulary.to_db()
        return  # MixedLanguageMessage(message, "Student", english, translated, vocabulary.language)
    except Exception as e:
        print("Error:", e)
        print("Response:", response)
        print("Prompt:", message.text)
        return  # MixedLanguageMessage(message, "Student", None, None, vocabulary.language)


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
