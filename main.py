from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import groq 

app = FastAPI(
    title="ReiletAI",
    description="API de détection de vishing.",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

# Your existing routes here

# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# app.include_router(mode.router, prefix="/api/mode", tags=["mode"])
app.include_router(groq.router, prefix="/api/groq", tags=["groq"])

@app.get("/")
def read_root():
    return {"message": "Welcome to ReiletAI API"}