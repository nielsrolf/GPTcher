import json
import os
import requests

req_url = "https://api.openai.com/v1/engines/audio-transcribe-001/transcriptions"
openai_key = os.getenv("OPENAI_API_KEY")



file_path = "/Users/nielswarncke/Documents/code/gptcher/data/speech/2023-01-06 19.25.47.ogg"
file = open(file_path, "rb")

headers = {
    "Authorization": f"Bearer {openai_key}",
    "Content-Type": "multipart/form-data",
}

data = {"file": (file_path, file, "audio/mpeg")}

response = requests.post(req_url, headers=headers, files=data)

response_data = json.loads(response.text)
print(response_data)