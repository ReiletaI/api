from fastapi import APIRouter
from app.services.groq import GroqService
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()

class TranscribeRequest(BaseModel):
    audio: str
    roomId: str = None  # Optional field
    roomStatus: str = None  # Optional field

@router.post("/transcribe")
async def transcribe(request: TranscribeRequest):
    groq_service = GroqService(settings.GROQ_API_KEY)
    return groq_service.transcribe(request.audio, request.roomId, request.roomStatus)

@router.post("/detect_vishing")
async def detect_vishing(transcription_file: str):
    groq_service = GroqService(settings.GROQ_API_KEY)
    return groq_service.detect_vishing(transcription_file)
