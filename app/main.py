from fastapi import FastAPI
from app.api.endpoints import chat, mode

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

@app.get("/")
def read_root():
    return {"message": "Welcome to AIChatHub API"}
