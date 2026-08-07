from fastapi import APIRouter, HTTPException
from app.services.data_service import data_service
from app.services.model_service import model_service

router=APIRouter(prefix="/root-cause",tags=["Root Cause Graph"])

@router.get("/{student_id}")
def root_cause(student_id:str):
    row=data_service.student(student_id)
    if not row: raise HTTPException(404,"Student not found")
    exp=model_service.explain_one(row,12)
    nodes=[{"id":"risk","label":"Dropout Risk","type":"outcome"}]
    edges=[]
    for i,f in enumerate(exp["top_factors"]):
        nid=f"f{i}"; nodes.append({"id":nid,"label":f["feature"],"type":"risk_factor","value":f["value"],"direction":f["direction"]})
        edges.append({"source":nid,"target":"risk","weight":f["impact"],"direction":f["direction"]})
    return {"student_id":student_id,"nodes":nodes,"edges":edges}
