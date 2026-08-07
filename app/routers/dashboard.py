from fastapi import APIRouter
from app.services.data_service import data_service
from app.services.model_service import model_service
from app.services.fairness_service import fairness_report
from app.services.resource_service import allocation_plan

router=APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def summary(district: str | None = None):
    return data_service.summary(district)

@router.get("/risk-trend")
def risk_trend():
    return data_service.risk_trend()

@router.get("/top-risk-factors")
def top_factors(limit: int = 10):
    df=data_service.dataframe()
    try: return {"factors":model_service.global_feature_importance(df, top_k=min(max(limit,1),30))}
    except Exception as e: return {"factors":[],"error":str(e)}

@router.get("/alerts")
def alerts():
    return {"alerts":data_service.alerts()}

@router.get("/overview")
def overview(district: str | None = None):
    return {
        "summary":data_service.summary(district),
        "risk_trend":data_service.risk_trend(),
        "alerts":data_service.alerts(),
        "districts":data_service.districts()[:10],
        "fairness":fairness_report()["summary"],
        "resource_allocation":allocation_plan(100000, district),
        "model_status":model_service.status(),
    }
