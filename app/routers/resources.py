from fastapi import APIRouter
from app.services.resource_service import allocation_plan
router=APIRouter(prefix="/resources",tags=["Resource Allocation"])
@router.get("/allocation")
def allocation(budget: float=100000,district: str|None=None): return allocation_plan(budget,district)
