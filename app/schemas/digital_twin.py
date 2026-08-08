from typing import List, Optional
from pydantic import BaseModel, Field


class RiskFactor(BaseModel):
    factor: str
    value: str
    impact: str
    contribution: float


class DigitalTwinRequest(BaseModel):
    student_id: Optional[str] = Field(
        default=None,
        description="Optional student identifier",
    )

    attendance_rate: float = Field(
        ...,
        ge=0,
        le=100,
        description="Student attendance percentage",
    )

    average_test_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Average academic test score",
    )

    household_income: float = Field(
        ...,
        ge=0,
        description="Annual household income",
    )

    distance_to_school: float = Field(
        ...,
        ge=0,
        description="Distance from home to school in kilometres",
    )

    internet_access: bool = Field(
        ...,
        description="Whether the student has internet access",
    )

    behavioural_incidents: int = Field(
        default=0,
        ge=0,
        description="Number of recorded behavioural incidents",
    )


class DigitalTwinResponse(BaseModel):
    student_id: str

    risk_probability: float
    risk_score: float
    risk_level: str
    confidence_score: float

    attendance_rate: float
    average_test_score: float
    household_income: float
    distance_to_school: float
    internet_access: bool
    behavioural_incidents: int

    academic_status: str
    attendance_status: str
    socioeconomic_status: str
    digital_access_status: str

    top_risk_factors: List[RiskFactor]

    recommendation: str

    engine: str = "VIZHIPPAAN AI Student Digital Twin"
