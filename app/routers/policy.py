from fastapi import APIRouter
from app.services.data_service import data_service

router=APIRouter(prefix="/policy",tags=["Policy Simulator"])

@router.get("/baseline")
def baseline():
    return {"summary":data_service.summary(),"districts":data_service.districts()}

@router.post("/simulate")
def simulate_policy(scholarship_coverage_increase_pct:float=0, attendance_program_reach_pct:float=0):
    # This endpoint deliberately labels its result as a planning scenario, not causal inference.
    s=data_service.summary(); high=s["risk"]["High"]["count"]+s["risk"]["Critical"]["count"]
    assumed=(max(0,min(scholarship_coverage_increase_pct,100))*0.0015 + max(0,min(attendance_program_reach_pct,100))*0.0020)
    reduction=min(high, round(high*assumed))
    return {"baseline_high_or_critical":high,"scenario_estimated_students_improved":reduction,"assumptions":{"scholarship_coverage_increase_pct":scholarship_coverage_increase_pct,"attendance_program_reach_pct":attendance_program_reach_pct},"method_note":"Illustrative policy scenario based on explicit assumptions; not causal evidence."}
