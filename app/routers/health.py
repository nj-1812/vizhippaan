from datetime import datetime, timezone
from fastapi import APIRouter
from app.services.model_service import model_service
from app.services.data_service import data_service

router=APIRouter(tags=["System"])

@router.get("/health")
def health():
    model=model_service.status(); data=data_service.status()
    healthy=model["loaded"] and data["loaded"]
    return {
        "status":"healthy" if healthy else "degraded",
        "model":model,
        "data":data,
        "api":"healthy",
        "timestamp":datetime.now(timezone.utc).isoformat(),
    }
