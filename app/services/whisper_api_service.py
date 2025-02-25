import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

class WhisperAPIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key is None:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        self.api_url = "https://api.openai.com/v1/audio/transcriptions"

    def transcribe(self, audio_path: str):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        with open(audio_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {
                "model": "whisper-1",
                "response_format": "json",
                "language": "en"
            }
            response = requests.post(self.api_url, headers=headers, files=files, data=data)
            response.raise_for_status()
            return response.json()["text"]

    def verify_api_key(self):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        response = requests.get("https://api.openai.com/v1/models", headers=headers)
        return response.status_code == 200
