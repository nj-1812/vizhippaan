from fastapi import APIRouter, HTTPException
from app.schemas import InterventionRequest
from app.services.data_service import data_service
from app.services.intervention_service import INTERVENTIONS, simulate

router=APIRouter(prefix="/interventions", tags=["Interventions"])

@router.get("/catalog")
def catalog():
    return {"interventions":list(INTERVENTIONS.keys())}

@router.post("/simulate")
def intervention_simulator(payload: InterventionRequest):
    features=payload.features
    if payload.student_id:
        features=data_service.student(payload.student_id)
        if not features: raise HTTPException(404,"Student not found")
    if not features: raise HTTPException(400,"Provide student_id or features")
    try: return simulate(features,payload.interventions)
    except Exception as e: raise HTTPException(400,str(e))
