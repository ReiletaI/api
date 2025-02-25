from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.whisper_api_service import WhisperAPIService
import tempfile

router = APIRouter()
whisper_api_service = WhisperAPIService()

@router.post("/transcribe-api")
async def transcribe_api_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name

    try:
        translation = whisper_api_service.transcribe(temp_audio_path)
        return {"translation": translation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
