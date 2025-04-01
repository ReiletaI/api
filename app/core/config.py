from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os
from functools import lru_cache

class Settings(BaseSettings):
    # Your settings here
    APP_NAME: str = "ReiletAI"
    HF_TOKEN: str = os.getenv("HF_TOKEN")  # Default or from env
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    RECORDINGS_PATH: str = os.path.join(os.getcwd(), "Audios")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Create and cache settings"""
    return Settings()
