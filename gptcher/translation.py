import json
import requests
import json
from gptcher.language_codes import code_of

from google.cloud import translate_v2 as translate


def _google_translate(target_language, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    print(f"Translating {text} to {target_language}...")
    if len(target_language) < 4:
        target_language = code_of[target_language]
    translate_client = translate.Client()
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]


def _deepl_translate(target_language, text):
    language_code = code_of[target_language]
    target_lang = language_code.split("-")[0].upper()

    url = "https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs"
    headers = {'Content-Type': 'application/json'}


    payload = {"jsonrpc":"2.0","method": "LMT_handle_jobs","params":{"jobs":[{"kind":"default","sentences":[{"text": text,"id":0,"prefix":""}],"raw_en_context_before":[],"raw_en_context_after":[],"preferred_num_beams":4,"quality":"fast"}],"lang":{"preference":{"weight":{"DE":1.58675,"EN":14.42718,"ES":6.00943,"FR":0.05474,"IT":0.02754,"JA":0.01262,"NL":0.3008,"PL":0.01711,"PT":0.01209,"RU":0.00541,"ZH":0.00905,"BG":0.0009,"CS":0.00448,"DA":0.00574,"EL":0.00017,"ET":0.00654,"FI":0.00507,"HU":0.00489,"ID":0.01427,"LV":0.00243,"LT":0.00326,"RO":0.00766,"SK":0.00482,"SL":0.01086,"SV":0.00848,"TR":0.00427,"UK":0.00021},"default":"default"},"source_lang_user_selected":"auto","target_lang": target_lang},"priority":-1,"commonJobParams":{"mode":"translate","browserType":1},"timestamp":1674311668356},"id":49140032}
    data = json.dumps(payload)
    response = requests.post(url, headers=headers, data=data)

    data = response.json()

    translations = []
    for beam in data['result']['translations'][0]['beams']:
        translations.append(beam['sentences'][0]['text'])
    return translations


def translate(text, target_language):
    try:
        return _deepl_translate(target_language, text)
    except:
        return [_google_translate(target_language, text)]
