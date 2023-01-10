import boto3
from gptcher.language_codes import code_of
import os
import pandas as pd
from functools import cache
import random
from dotenv import load_dotenv
from gptcher.utils import hash_string, supabase
import io

load_dotenv(override=True)


@cache
def load_voices():
    """loads the voices from the file polly_voices.csv in the same dir as this file"""
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "polly_voices.csv"))
    return df


def select_voice(language):
    voices = load_voices()
    lan = code_of[language]
    codes_to_try = [f"{lan}-{lan.upper()}", f"{lan}-US", "en-US"]
    for code in codes_to_try:
        if code in voices["Language code"].values:
            break
    voices = voices.loc[voices["Language code"] == code].iloc[0]
    available_voices = []
    engine = "neural"
    for voice, has_neural in zip(
        voices["Name/ID"].split("\n"), voices["Neural Voice"].split("\n")
    ):
        if has_neural == "Yes":
            available_voices.append(voice)
    if len(available_voices) == 0:
        available_voices = voices["Name/ID"].split("\n")
        engine = "standard"
    voice = random.choice(available_voices)
    return voice, engine


def read_and_save_voice(text, language):
    print(text)
    filename = hash_string(text + language)[:7] + ".ogg"
    voice, engine = select_voice(language)
    if voice_url := check_if_exists_in_s3(filename):
        return voice_url

    polly = boto3.client("polly")
    filename_mp3 = filename.replace(".ogg", ".mp3")
    response = polly.synthesize_speech(
        Text='<speak><prosody rate="-25%">' + text + "</prosody></speak>",
        TextType="ssml",
        OutputFormat="mp3",
        VoiceId=voice,
        Engine=engine,
    )
    # Save the audio stream returned by Amazon Polly
    with open(filename_mp3, "wb") as f:
        f.write(response["AudioStream"].read())
    # os.system(f"ffmpeg -y -i {filename_mp3}  -vn -acodec libvorbis {filename}")
    return save_to_s3(filename_mp3)


def check_if_exists_in_s3(filename):
    s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket="gptcher", Key=filename)
        return f"https://gptcher.s3.eu-central-1.amazonaws.com/{filename}"
    except:
        pass
    return False


def save_to_s3(filename):
    s3 = boto3.client("s3")
    s3.upload_file(filename, "gptcher", filename)
    return f"https://gptcher.s3.eu-central-1.amazonaws.com/{filename}"


def create_for_all_existing():
    tasks = supabase.from_("translation_tasks").select("*").execute().data
    for task in tasks:
        if task["voice"] is None:
            voice_url = read_and_save_voice(
                task["sentence_translated"], task["language"]
            )
            supabase.table("translation_tasks").update({"voice": voice_url}).eq(
                "id", task["id"]
            ).execute()
            print(f"created voice for {task['id']}: {voice_url}")
        else:
            print(f"skipped {task['id']}")
    return "done"


if __name__ == "__main__":
    create_for_all_existing()
