from fastapi import APIRouter, HTTPException, Query
from app.services.data_service import data_service
from app.services.model_service import model_service

router=APIRouter(prefix="/students", tags=["Students"])

@router.get("")
def list_students(q: str="", risk_level: str|None=None, district: str|None=None, limit: int=Query(50,ge=1,le=200)):
    return {"students":data_service.student_list(q,risk_level,district,limit)}

@router.get("/{student_id}")
def get_student(student_id: str):
    row=data_service.student(student_id)
    if not row: raise HTTPException(404,"Student not found")
    result={"student":row}
    try: result["prediction"]=model_service.predict_one(row)
    except Exception as e: result["prediction_error"]=str(e)
    return result

@router.get("/{student_id}/risk")
def student_risk(student_id: str):
    row=data_service.student(student_id)
    if not row: raise HTTPException(404,"Student not found")
    try: return {"student_id":student_id, **model_service.predict_one(row)}
    except Exception as e: raise HTTPException(400,str(e))

@router.get("/{student_id}/explanation")
def student_explanation(student_id: str, top_k: int=10):
    row=data_service.student(student_id)
    if not row: raise HTTPException(404,"Student not found")
    try: return {"student_id":student_id, **model_service.explain_one(row,min(max(top_k,1),30))}
    except Exception as e: raise HTTPException(400,str(e))

@router.get("/{student_id}/digital-twin")
def digital_twin(student_id: str):
    row=data_service.student(student_id)
    if not row: raise HTTPException(404,"Student not found")
    prediction=model_service.predict_one(row)
    explanation=model_service.explain_one(row,8)
    return {
        "student_id":student_id,
        "profile":row,
        "current_risk":prediction,
        "explanation":explanation,
        "digital_twin_note":"Current-state digital twin generated from the latest available student record.",
    }
