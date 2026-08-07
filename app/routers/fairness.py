from fastapi import APIRouter
from app.services.fairness_service import fairness_report
router=APIRouter(prefix="/fairness",tags=["Responsible AI"])
@router.get("/report")
def report(): return fairness_report()
