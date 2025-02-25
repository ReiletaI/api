from fastapi import APIRouter, HTTPException
from app.services.whisper_api_service import WhisperAPIService

router = APIRouter()
whisper_api_service = WhisperAPIService()

@router.get("/verify-api-key")
async def verify_api_key():
    try:
        is_valid = whisper_api_service.verify_api_key()
        return {"valid": is_valid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
