from fastapi import FastAPI
from app.api.endpoints import chat, transcription_api, transcription_local, verify_api_key

app = FastAPI(
    title="ReiletAI",
    description="API de détection de vishing.",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# app.include_router(mode.router, prefix="/api/mode", tags=["mode"])
app.include_router(transcription_local.router, prefix="/api/transcription", tags=["transcription"])
app.include_router(transcription_api.router, prefix="/api/transcription", tags=["transcription"])
app.include_router(verify_api_key.router, prefix="/api", tags=["utilities"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AIChatHub API"}