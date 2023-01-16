from gptcher.language_codes import code_of
from gptcher.utils import measure_time, print_times
import os
import banana_dev as banana
from dotenv import load_dotenv

load_dotenv(override=True)


@measure_time
def transcribe(file_url, language):
    language_code = code_of[language]
    model_key = "86b4a6b0-425f-4767-9ce9-faf62a0b8ca2"
    banana_api_key = os.environ['BANANA_API_KEY']
    model_payload = {
        "audio": file_url,
        "language": language_code,
    }
    out = banana.run(banana_api_key, model_key, model_payload)
    return out['modelOutputs'][0]['transcription'].strip()


