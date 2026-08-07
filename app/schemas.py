from typing import Any
from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    features: dict[str, Any] = Field(..., description="Feature dictionary matching model_metadata.json")

class BatchPredictRequest(BaseModel):
    rows: list[dict[str, Any]]

class InterventionRequest(BaseModel):
    student_id: str | None = None
    features: dict[str, Any] | None = None
    interventions: list[str] = Field(default_factory=list)

class StudentSearchRequest(BaseModel):
    query: str = ""
    risk_level: str | None = None
    district: str | None = None
    limit: int = Field(25, ge=1, le=200)

class ResourceRequest(BaseModel):
    budget: float = Field(100000, gt=0)
    district: str | None = None
