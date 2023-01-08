import hashlib
import json
import os

import openai
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")
url = os.getenv("SUPABASE_URL")
supabase_api_key = os.getenv("SUPABASE_API_KEY")
supabase = create_client(url, supabase_api_key)


time_in_functions = {}


def measure_time(func):
    def wrapper(*args, **kwargs):
        import time

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time for {func.__name__}: {end - start}")
        if func.__name__ not in time_in_functions:
            time_in_functions[func.__name__] = [end - start]
        else:
            time_in_functions[func.__name__].append(end - start)
        return result

    return wrapper


def print_times():
    for name, times in time_in_functions.items():
        print(f"{name}: {len(times)} x {sum(times)/len(times)}")


def complete_without_hash(prompt, stop, max_tokens=256):
    print("Prompt:\n\n", prompt, "\n\nStop:\n\n", stop, "\n\n")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=stop,
    )
    response = response.choices[0].text
    return response


def hash_string(s: str) -> str:
    h = hashlib.sha256()
    h.update(s.encode())
    return h.hexdigest()


def complete_with_hash(prompt, stop, max_tokens=256, override=False):
    prompt_hash = hash_string(prompt)
    if not override:
        completions = (
            supabase.table("completions")
            .select("*")
            .eq("prompt_hash", prompt_hash)
            .execute()
            .data
        )
        if len(completions) > 0:
            response = completions[0]["response"]
            return response
    response = complete_without_hash(prompt, stop, max_tokens)
    if max_tokens > 1000:
        max_tokens = 1000
    supabase.table("completions").upsert(
        {"prompt_hash": prompt_hash, "response": response}
    ).execute()
    return response


def complete(prompt, stop, prefix="", max_tokens=256, override=False):
    prompt = prompt + prefix
    response = complete_with_hash(prompt, stop, max_tokens, override)
    return prefix + response


def complete_and_parse_json(prompt, stop, prefix="", max_tokens=256):
    override = False
    for attempt in range(3):
        response = complete(prompt, stop, prefix, max_tokens, override)
        for i in range(10):
            print("...", response)
            try:
                data = json.loads(response)
                return data
            except json.decoder.JSONDecodeError:
                response = complete(prompt, stop, response, max_tokens)
        override = True
    breakpoint()
