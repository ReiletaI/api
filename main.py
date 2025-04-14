import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.diarization import DiarizationService
from app.core.config import get_settings

app = FastAPI(
    title="ReiletAI",
    description="API de détection de vishing.",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)
settings = get_settings()

# Initialize the DiarizationService with the Hugging Face token
diarization_service = DiarizationService(settings.HF_TOKEN)

# Check if GPU is available
if torch.cuda.is_available():
    torch.cuda.empty_cache()  # Clear GPU memory
    print("GPU is available for processing.")
else:
    print("GPU is not available. Using CPU.")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a dependency function to get the diarization service
def get_diarization_service():
    return diarization_service

# Import endpoints here (AFTER defining diarization_service)
from app.api.endpoints import groq, data

# Include router
app.include_router(groq.router, prefix="/api/v1")
app.include_router(data.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to ReiletAI API"}

# Override the dependency
app.dependency_overrides[groq.get_diarization_service] = get_diarization_service