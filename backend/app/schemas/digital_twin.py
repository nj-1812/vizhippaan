from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class StudentTwinRequest(BaseModel):
    # Student identity
    student_id: str = Field(..., examples=["STU78291"])

    student_name: Optional[str] = Field(
        default="Student"
    )

    grade: Optional[str] = Field(
        default=None
    )

    school_name: Optional[str] = Field(
        default=None
    )

    district: Optional[str] = Field(
        default=None
    )

    # =========================================================
    # MODEL FEATURES
    # These must match your current prediction API
    # =========================================================

    attendance_rate: float = Field(
        ...,
        ge=0,
        le=100
    )

    average_test_score: float = Field(
        ...,
        ge=0,
        le=100
    )

    household_income: float = Field(
        ...,
        ge=0
    )

    distance_to_school: float = Field(
        ...,
        ge=0
    )

    internet_access: bool

    behavioural_incidents: int = Field(
        default=0,
        ge=0
    )

    # Optional live information

    previous_attendance_rate: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )

    previous_test_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )


class RiskDriver(BaseModel):
    factor: str

    impact: float

    severity: str

    direction: str

    explanation: str


class HorizonRisk(BaseModel):
    horizon: str

    probability: float

    risk_level: str


class Recommendation(BaseModel):
    title: str

    priority: str

    reason: str


class StudentTwinResponse(BaseModel):
    student_id: str

    student_name: str

    grade: Optional[str]

    school_name: Optional[str]

    district: Optional[str]

    current_risk: Dict[str, Any]

    learning_stability_score: float

    confidence_score: float

    horizons: List[HorizonRisk]

    risk_drivers: List[RiskDriver]

    recommendations: List[Recommendation]

    live_metrics: Dict[str, Any]

    model_status: str

    projection_method: str

    generated_at: str
