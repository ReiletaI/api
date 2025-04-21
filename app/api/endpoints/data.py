from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.call_analysis import CallAnalysisDB
from app.database import get_db
import asyncio
from sqlalchemy import func

router = APIRouter()

@router.post("/upload")
async def upload_voice_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Simuler le traitement du fichier
        await asyncio.sleep(1)
        
        # Créer une nouvelle analyse d'appel
        new_analysis = CallAnalysisDB(
            fileName=file.filename,
            dateAnalyzed=datetime.now().isoformat(),
            status="pending",
            threatLevel="unknown",
            callerNumber="+33612345678",  # À remplacer par la vraie détection
            recipientNumber="+33687654321"  # À remplacer par la vraie détection
        )
        
        db.add(new_analysis)
        db.commit()
        db.refresh(new_analysis)
        
        return {"success": True, "message": "File uploaded and analysis started.", "analysis_id": new_analysis.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    total_calls = db.query(func.count(CallAnalysisDB.id)).scalar() or 0
    threats_detected = db.query(func.count(CallAnalysisDB.id)).filter(CallAnalysisDB.threatLevel != "low").scalar() or 0
    threats_verified = db.query(func.count(CallAnalysisDB.id)).filter(CallAnalysisDB.status == "verified").scalar() or 0
    pending_verification = db.query(func.count(CallAnalysisDB.id)).filter(CallAnalysisDB.status == "pending").scalar() or 0
    return {
        "totalCallsAnalyzed": total_calls,
        "threatsDetected": threats_detected,
        "threatsVerified": threats_verified,
        "pendingVerification": pending_verification
    }

@router.get("/monthly/data")
async def get_monthly_data(db: Session = Depends(get_db)):
    # Group by month and count
    results = db.query(CallAnalysisDB.dateAnalyzed, func.count(CallAnalysisDB.id))\
        .group_by(func.strftime("%Y-%m", CallAnalysisDB.dateAnalyzed))\
        .all()
    # Format: [{"month": "YYYY-MM", "callsAnalyzed": count}, ...]
    monthly_stats = []
    for date_str, count in results:
        month = date_str[:7] if date_str else ""
        monthly_stats.append({"month": month, "callsAnalyzed": count})
    if not monthly_stats:
        return []
    return monthly_stats

@router.get("/recent/detections")
async def get_recent_detections(limit: int = 5, db: Session = Depends(get_db)):
    results = db.query(CallAnalysisDB).order_by(CallAnalysisDB.dateAnalyzed.desc()).limit(limit).all()
    return [r.as_dict() for r in results]

@router.post("/analysis")
async def add_analysis(analysis: dict, db: Session = Depends(get_db)):
    db_analysis = CallAnalysisDB(**analysis)
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis.as_dict()

@router.get("/analysis")
async def get_all_analyses(db: Session = Depends(get_db)):
    results = db.query(CallAnalysisDB).order_by(CallAnalysisDB.dateAnalyzed).all()
    return [r.as_dict() for r in results]