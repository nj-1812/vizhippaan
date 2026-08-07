from fastapi import APIRouter
from app.services.data_service import data_service
from app.services.model_service import model_service

router=APIRouter(prefix="/quality",tags=["App Quality Guardian"])

@router.get("")
def quality():
    df=data_service.dataframe()
    missing_pct=round(float(df.isna().mean().mean()*100),2) if not df.empty else None
    duplicates=int(df.duplicated().sum()) if not df.empty else None
    return {"model":model_service.status(),"data":data_service.status(),"data_quality":{"overall_missing_pct":missing_pct,"duplicate_rows":duplicates},"checks":{"api":"pass","model_loaded":"pass" if model_service.loaded else "fail","dataset_loaded":"pass" if not df.empty else "fail"}}
