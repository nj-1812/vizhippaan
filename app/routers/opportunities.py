from fastapi import APIRouter
import pandas as pd
from app.services.data_service import data_service

router=APIRouter(prefix="/opportunities",tags=["Opportunity Detector"])

@router.get("")
def opportunities(limit:int=100):
    df=data_service.dataframe().copy()
    if df.empty: return {"count":0,"students":[]}
    risk=data_service._risk_series(df)
    mask=risk.isin(["Medium","High"])
    if "attendance_rate_pct" in df.columns: mask &= pd.to_numeric(df["attendance_rate_pct"],errors="coerce").fillna(0) >= 60
    if "average_test_score_pct" in df.columns: mask &= pd.to_numeric(df["average_test_score_pct"],errors="coerce").fillna(0) >= 50
    subset=df[mask].head(max(1,min(limit,500)))
    ids=subset["student_id"].astype(str).tolist() if "student_id" in subset.columns else [str(i) for i in subset.index]
    return {"count":int(mask.sum()),"students":ids,"definition":"Medium/High risk students with comparatively recoverable attendance and academic signals."}
