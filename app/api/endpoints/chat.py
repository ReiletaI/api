from fastapi import APIRouter, Depends
from app.services.groq import GroqService
from app.core.config import settings

router = APIRouter()

