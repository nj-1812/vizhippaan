from fastapi import APIRouter, HTTPException
from app.schemas import PredictRequest, BatchPredictRequest
from app.services.model_service import model_service

router=APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("")
def predict(payload: PredictRequest):
    try: return model_service.predict_one(payload.features)
    except Exception as e: raise HTTPException(400, str(e))

@router.post("/batch")
def batch_predict(payload: BatchPredictRequest):
    try: return {"count":len(payload.rows),"predictions":model_service.predict_rows(payload.rows)}
    except Exception as e: raise HTTPException(400, str(e))

@router.get("/schema")
def prediction_schema():
    return {"features":model_service.features,"categorical":model_service.categorical}
