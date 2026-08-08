from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DigitalTwinRequest(BaseModel):
    student_id: str = Field(default="STU78291")
    student_name: str = Field(default="Student")

    grade: Optional[str] = None
    school_name: Optional[str] = None
    district: Optional[str] = None

    attendance_rate: float = Field(..., ge=0, le=100)
    average_test_score: float = Field(..., ge=0, le=100)

    household_income: float = Field(..., ge=0)
    distance_to_school: float = Field(..., ge=0)

    internet_access: bool

    behavioural_incidents: int = Field(
        default=0,
        ge=0,
    )

    previous_attendance_rate: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )

    previous_test_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )


class HorizonPrediction(BaseModel):
    horizon: str
    probability: float
    risk_level: str


class RiskDriver(BaseModel):
    factor: str
    impact: float
    severity: str
    explanation: str


class InterventionRecommendation(BaseModel):
    title: str
    priority: str
    reason: str
    expected_effect: str


class DigitalTwinResponse(BaseModel):
    student_id: str
    student_name: str

    grade: Optional[str]
    school_name: Optional[str]
    district: Optional[str]

    current_risk: Dict[str, Any]

    learning_stability_score: float
    confidence_score: float

    horizons: List[HorizonPrediction]

    risk_drivers: List[RiskDriver]

    recommendations: List[InterventionRecommendation]

    live_metrics: Dict[str, Any]

    model_status: str
    generated_at: str
