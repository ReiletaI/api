from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from datetime import datetime
import json
from app.models.init import CallAnalysis, DashboardStats, MonthlyData
import asyncio

router = APIRouter()

# Mock data
call_analyses: List[CallAnalysis] = [
    {
        "id": "1",
        "fileName": "call_20240413_1200.wav",
        "dateAnalyzed": "2024-04-13T12:00:00",
        "status": "verified",
        "threatLevel": "high",
        "callerNumber": "+33612345678",
        "recipientNumber": "+33687654321"
    },
    {
        "id": "2",
        "fileName": "call_20240413_1300.wav",
        "dateAnalyzed": "2024-04-13T13:00:00",
        "status": "pending",
        "threatLevel": "medium",
        "callerNumber": "+33698765432",
        "recipientNumber": "+33612345678"
    }
]

dashboard_stats: DashboardStats = {
    "totalCallsAnalyzed": 100,
    "threatsDetected": 25,
    "threatsVerified": 20,
    "pendingVerification": 5
}

monthly_data: List[MonthlyData] = [
    {"month": "2024-04", "callsAnalyzed": 50},
    {"month": "2024-03", "callsAnalyzed": 45},
    {"month": "2024-02", "callsAnalyzed": 40},
    {"month": "2024-01", "callsAnalyzed": 35}
]

@router.post("/upload")
async def upload_voice_file(file: UploadFile = File(...)):
    try:
        # Simuler le traitement du fichier
        await asyncio.sleep(1)
        return {"success": True, "message": "File uploaded and analyzed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    return dashboard_stats

@router.get("/monthly/data", response_model=List[MonthlyData])
async def get_monthly_data():
    return monthly_data

@router.get("/recent/detections", response_model=List[CallAnalysis])
async def get_recent_detections(limit: int = 5):
    return call_analyses[:limit]