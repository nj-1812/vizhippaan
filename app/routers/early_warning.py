from fastapi import APIRouter
from app.services.data_service import data_service

router=APIRouter(prefix="/early-warning",tags=["Early Warning"])

@router.get("")
def early_warning(limit:int=100):
    df=data_service.dataframe().copy()
    if df.empty: return {"count":0,"students":[]}
    risk=data_service._risk_series(df)
    candidates=df[risk.isin(["High","Critical"])].copy()
    ids=candidates["student_id"].astype(str).head(max(1,min(limit,500))).tolist() if "student_id" in candidates.columns else []
    return {"count":int(len(candidates)),"students":ids,"horizon":"current available snapshot"}
