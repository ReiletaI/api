import requests
from groq import Groq
import base64
import os
import json
import datetime
import subprocess
import uuid
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self, api_key, diarization_service=None):
        logger.info("Initializing GroqService")
        self.api_key = api_key
        self.base_url = "https://api.groq.ai"
        self.client = Groq(api_key=api_key)  # Ensure Groq class accepts api_key
        self.recordings_path = os.path.join(os.getcwd(), "Audios")  # Assuming recordings path is set here
        os.makedirs(self.recordings_path, exist_ok=True)
        self.diarization_service = diarization_service
        logger.info(f"Diarization service: {diarization_service is not None}")

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
    
    def convert_webm_to_wav(self, input_path, output_path):
        """Convert webm audio file to wav format for processing"""
        command = [
            'ffmpeg',
            '-i', input_path,
            '-ar', '16000',
            '-ac', '1',
            output_path
        ]
        subprocess.run(command, check=True)
        return output_path
    
    def transcribe(self, audio_client, audio_support, room_id, room_status):
        logger.info(f"Starting transcription for room {room_id}")
        """
        Process both client and support audio streams for transcription
        
        Args:
            data (dict): Dictionary containing:
                - audio_client: Base64 encoded client audio (optional)
                - audio_support: Base64 encoded support audio (optional)
                - roomId: Room identifier
                - roomStatus: Current room status
                
        Returns:
            dict: Transcription result with text, success status, and source
        """
                
        # Check if call is in progress
        if room_status != "Connected":
            return {
                "text": "No call in progress.",
                "success": False,
                "source": "system"
            }

        # Check if at least one audio stream is provided
        if not audio_client and not audio_support:
            return {
                "text": "No audio data provided.",
                "success": False,
                "source": "system"
            }

        try:
            client = self.client
            audio_model = "whisper-large-v3"
            # Prepare directory structure
            timestamp = datetime.datetime.now().strftime('%Y%m%d')
            folder = os.path.join(self.recordings_path, f"{timestamp}")
            
            os.makedirs(folder, exist_ok=True)
            
            room_dir = os.path.join(folder, f"{room_id}")
            os.makedirs(room_dir, exist_ok=True)
            
            combined_segments = []
            combined_segments_support = []
            combined_segments_client = []
            
            # Process client audio if available
            if audio_client:
                try:
                    header, encoded = audio_client.split(",", 1)
                    client_audio_data = base64.b64decode(encoded)
                    
                    # Save client audio
                    filename_client = os.path.join(room_dir, f"chunk_{timestamp}_{room_id}_client.webm")
                    with open(filename_client, "wb") as f:
                        f.write(client_audio_data)
                    
                    # Convert WebM to WAV
                    filename_client_wav = self.convert_webm_to_wav(
                        filename_client, 
                        os.path.join(room_dir, f"chunk_{timestamp}_{room_id}_client_{str(uuid.uuid4())[:8]}.wav")
                    )
                    
                    # Perform diarization if service is available
                    if self.diarization_service:
                        try:
                            diarization_result = self.diarization_service.perform_diarization(filename_client_wav)
                            print(f"Client audio diarization: {len(diarization_result)} segments")
                        except Exception as d_error:
                            print(f"Diarization error on client audio: {d_error}")
                    
                    # Transcribe client audio
                    with open(filename_client_wav, "rb") as audio_file:
                        translation = self.client.audio.transcriptions.create(
                            file=audio_file,
                            model=audio_model,
                            response_format="verbose_json",
                        )
                    
                    client_transcribed_data = json.loads(translation.model_dump_json())
                    
                    # Process client segments
                    client_segments = client_transcribed_data.get('segments', [])
                    for segment in client_segments:
                        start_time = segment.get('start', 0)
                        end_time = segment.get('end', 0)
                        text = segment.get('text', '').strip()
                        
                        if text:
                            combined_segments_client.append({
                                "start": start_time,
                                "end": end_time,
                                "sourceType": "Caller",
                                "text": text
                            })
                except Exception as e:
                    print(f"Error processing client audio: {e}")
            
            # Process support audio if available
            if audio_support:
                try:
                    header, encoded = audio_support.split(",", 1)
                    support_audio_data = base64.b64decode(encoded)
                    
                    # Save support audio
                    filename_support = os.path.join(room_dir, f"chunk_{timestamp}_{room_id}_support.webm")
                    with open(filename_support, "wb") as f:
                        f.write(support_audio_data)
                    
                    # Convert WebM to WAV
                    filename_support_wav = self.convert_webm_to_wav(
                        filename_support, 
                        os.path.join(room_dir, f"chunk_{timestamp}_{room_id}_support_{str(uuid.uuid4())[:8]}.wav")
                    )
                    
                    # Perform diarization if service is available
                    if self.diarization_service:
                        try:
                            diarization_result = self.diarization_service.perform_diarization(filename_support_wav)
                            print(f"Support audio diarization: {len(diarization_result)} segments")
                        except Exception as d_error:
                            print(f"Diarization error on support audio: {d_error}")
                    
                    # Transcribe support audio
                    with open(filename_support_wav, "rb") as audio_file:
                        translation = self.client.audio.transcriptions.create(
                            file=audio_file,
                            model=audio_model,
                            response_format="verbose_json",
                        )
                    
                    support_transcribed_data = json.loads(translation.model_dump_json())
                    
                    # Process support segments
                    support_segments = support_transcribed_data.get('segments', [])
                    for segment in support_segments:
                        start_time = segment.get('start', 0)
                        end_time = segment.get('end', 0)
                        text = segment.get('text', '').strip()
                        
                        if text:
                            combined_segments_support.append({
                                "start": start_time,
                                "end": end_time,
                                "sourceType": "Agent",
                                "text": text
                            })
                except Exception as e:
                    print(f"Error processing support audio: {e}")
            
            # Sort segments by start time
            combined_segments_client.sort(key=lambda x: x["start"])
            combined_segments_support.sort(key=lambda x: x["start"])
            
            # Write transcription to file and build response text
            transcribed_audio_path = os.path.join(room_dir, f"Transcription_{room_id}.txt")


            # Combine client and support segments
            combined_segments = combined_segments_client + combined_segments_support
            combined_segments.sort(key=lambda x: (x["start"], x["end"]))

            result_text = ""
            
            with open(transcribed_audio_path, 'a', encoding='utf-8') as audio_text:
                for segment in combined_segments:
                    line = f"{segment['sourceType']}: {segment['text']}"
                    audio_text.write(line + '\n')
                    result_text += line + '\n'
            
            # Analyze for vishing if segments exist
            if combined_segments and len(combined_segments) > 2:  # Only analyze if we have enough context
                try:
                    vishing_analysis = self.detect_vishing(transcribed_audio_path)
                    #result_text += f"\nAnalysis: {vishing_analysis}"
                except Exception as vish_error:
                    print(f"Error in vishing detection: {vish_error}")
        
            print(result_text)
            
            logger.info("Transcription completed successfully")
            return {
                "text": result_text,
                "analysis_result": vishing_analysis if 'vishing_analysis' in locals() else None,
                "success": True,
                "source": "transcription"
            }
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            logger.exception("Full exception details:")
            return {
                "text": f"Transcription failed: {str(e)}",
                "analysis_result": None,
                "success": False,
                "source": "error"
            }
        
    def detect_vishing(self, transcription_file):
        """
        Analyze transcript for signs of vishing (voice phishing)
        Returns classification as "Safe", "Suspect", or "Fraud"
        """
        client = self.client  # Use the stored client
        
        with open(transcription_file, "r", encoding='utf-8') as file:
            transcript = file.read()
        
        prompt = """
            You are an expert in detecting vishing (voice phishing) based on audio transcripts.

            The transcript provided contains a conversation between a caller and an agent. Your task is to analyze the transcript for any signs of vishing.
            The transcript can either be in English if the call is made in English or in French if the call is made in French. The language of the transcript will be indicated by the language of the text.
            The caller is the person who initiates the call, and the agent is the person who receives the call. The caller is the possible fraudster and the agent is the possible victim.
            
            Analyze the transcript for any indications of fraud or manipulation.
            Look for specific phrases, patterns, or behaviors that are commonly associated with vishing attempts.

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
            model="llama-3.3-70b-versatile",
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
            stream=False
        )

        output = completion.choices[0].message.content
        return output
