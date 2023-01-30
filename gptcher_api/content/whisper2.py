import requests
import os


openai_key = os.getenv("OPENAI_API_KEY")

url = "https://api.openai.com/v1/engines/audio-transcribe-001/transcriptions"
file_path = "audio.webm"

headers = {
    'Content-Type': 'multipart/form-data',
    "Authorization": f"Bearer {openai_key}",
}

with open(file_path, 'rb') as f:
    files = {'file': (file_path, f, 'video/webm')}
    response = requests.post(url, headers=headers, files=files, json={"language": "es-ES"})

print(response.text)