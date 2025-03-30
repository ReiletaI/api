import requests
from groq import Groq
import base64
import os
import json
import datetime

class GroqService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.groq.ai"
        self._client = Groq(api_key=api_key)  # Ensure Groq class accepts api_key
        self.recordings_path = "../../audios"  # Assuming recordings path is set here

    def get_response(self, query):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "query": query
        }
        response = requests.post(f"{self.base_url}/chat", headers=headers, json=data)
        return response.json()
    
    def transcribe(self, audio_path, room_id, room_status):
        if room_status != "Connected":
            return {"error": "No call in progress.", "text": ""}, 400

        if not audio_path:
            return {"error": "No audio data provided."}, 400

        try:
            client = Groq(api_key=self.api_key)  # Initialize Groq client
            audio_model = "whisper-large-v3"

            # Assuming audio_path is base64 encoded
            header, encoded = audio_path.split(",", 1)
            audio_data = base64.b64decode(encoded)  # Decode audio data

            # Create directory for recordings
            timestamp = datetime.datetime.now().strftime('%Y%m%d')
            folder = os.path.join(self.recordings_path, f"{timestamp}")

            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)

            room_dir = os.path.join(folder, f"{room_id}")

            if not os.path.exists(room_dir):
                os.makedirs(room_dir, exist_ok=True)

            # Naming audio and transcription files
            filename = os.path.join(room_dir, f"chunk_{timestamp}_{room_id}.webm")
            transcribed_audio = os.path.join(room_dir, f"Transcription_{room_id}.txt")

            # Save audio chunk
            with open(filename, "wb") as f:
                f.write(audio_data)

            # Transcription with Whisper on Groq
            with open(filename, "rb") as audio_file:
                translation = client.audio.translations.create(
                    file=audio_file,
                    model=audio_model,
                    response_format="verbose_json",
                )

            transcribed_data = json.loads(translation.model_dump_json())

            res = ""
            with open(transcribed_audio, 'a', encoding='utf-8') as audio_text:
                for segment in transcribed_data.get('segments', []):
                    line = segment.get('text', '').strip()
                    if line:
                        audio_text.write(line + '\n')
                        res += line + '\n'

                audio_text.write('[...]' + '\n')
                res += '[...]'

            return {"message": "Audio chunk saved.", "filename": str(filename), "text": res}
        except Exception as e:
            return {"error": f"Error saving audio chunk: {str(e)}"}, 500

    def detect_vishing(self, transcription_file):
        with open(transcription_file, "r") as file:
            transcript = file.read()
        
        prompt = """
            You are an expert in detecting vishing (voice phishing) based on audio transcripts.

            The transcript provided contains **only the client's speech**, and does not include any responses from the support agent.  
            Analyze the transcript for any indications of fraud or manipulation. Since the agent's responses are missing, focus on the client's words, tone, and requests.

            Consider factors such as:  
            - Urgency (e.g., pressuring for immediate action)  
            - Payment requests or unauthorized access attempts  
            - Usurpation (impersonation or stolen identity claims)  
            - Pressure tactics or authoritative language  
            - Evasive responses or inconsistencies  

            Based on your analysis, classify the transcript into one of three categories:  

            - **Safe**: No suspicious indicators.  
            - **Suspect**: Some indicators are present, but the evidence is inconclusive.  
            - **Fraud**: Clear signs of vishing fraud.  

            **Important:**  
            - Your response must be **only one word**: Safe, Suspect, or Fraud.  
            - Do not include any reasoning, explanations, or additional text.  
            """
        
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": transcript
                }
            ],
            temperature=0,
            max_completion_tokens=1024,
            top_p=0.95,
            stream=False,
            reasoning_format="parsed"
        )

        output = completion.choices[0].message.content
        return output
