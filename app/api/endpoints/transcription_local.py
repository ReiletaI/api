from fastapi import APIRouter, UploadFile, File
from app.services.whisper_local_service import WhisperLocalService
import tempfile

router = APIRouter()
whisper_local_service = WhisperLocalService("tiny")

@router.post("/transcribe-local")
async def transcribe_local_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name

    transcription = whisper_local_service.transcribe(temp_audio_path)
    return {"transcription": transcription}
