import requests

class GroqService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.groq.ai"

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
