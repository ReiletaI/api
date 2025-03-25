import requests
from groq import Groq

class GroqService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.groq.ai"
        self._client = Groq(api_key=api_key)  # Ensure Groq class accepts api_key

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
    
    def transcribe(self, audio_path):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        with open(audio_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {
                "model": "whisper-large-v3",
                "response_format": "venbose_json",
                "language": "en"
            }
            response = self._client.audio.transcriptions.create(files=files, data=data)
            return response.model_dump_json()

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
