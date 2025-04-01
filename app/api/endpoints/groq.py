from fastapi import APIRouter, Depends
from app.services.groq import GroqService
from app.core.config import get_settings
from pydantic import BaseModel
from typing import Callable

router = APIRouter()
settings = get_settings()

# Define a dependency function that will get the diarization_service
# The actual implementation is in main.py
def get_diarization_service():
    # This will be overridden by the actual function from main.py
    pass

class TranscribeRequest(BaseModel):
    audio_client: str = None  # Base64 encoded client audio
    audio_support: str = None  # Base64 encoded support audio
    roomId: str = None
    roomStatus: str = None

class SaveConversationRequest(BaseModel):
    audio: str = None  # Base64 encoded audio
    roomId: str = None
    roomStatus: str = None

@router.post("/transcribe")
async def transcribe(
    request: TranscribeRequest, 
    diarization_service = Depends(get_diarization_service)
):
    groq_service = GroqService(settings.GROQ_API_KEY, diarization_service)
    return groq_service.transcribe(
        request.audio_client, 
        request.audio_support, 
        request.roomId, 
        request.roomStatus
    )

@router.post("/detect_vishing")
async def detect_vishing(
    transcription_file: str, 
    diarization_service = Depends(get_diarization_service)
):
    groq_service = GroqService(settings.GROQ_API_KEY, diarization_service)
    return groq_service.detect_vishing(transcription_file)

#@router.post("/save_conversation")
#async def save_conversation(request: SaveConversationRequest):
#    groq_service = GroqService(settings.GROQ_API_KEY)
#    return groq_service.save_conversation(request.audio, request.roomId, request)

