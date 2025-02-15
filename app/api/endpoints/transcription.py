from fastapi import APIRouter, UploadFile, File
from app.services.whisper import WhisperService
import tempfile

router = APIRouter()
whisper_service = WhisperService("tiny")

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    # Créer un fichier temporaire pour stocker l'audio
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name

    # Transcrire l'audio
    transcription = whisper_service.transcribe(temp_audio_path)

    return {"transcription": transcription}