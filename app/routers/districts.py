from fastapi import APIRouter
from app.services.data_service import data_service
router=APIRouter(prefix="/districts",tags=["Districts & GIS"])
@router.get("/risk")
def district_risk(): return {"districts":data_service.districts()}
