from typing import List, Optional

from pydantic import BaseModel, Field


class HistoryPoint(BaseModel):
    period: str

    attendance_rate: float = Field(
        ...,
        ge=0,
        le=100,
    )

    average_test_score: float = Field(
        ...,
        ge=0,
        le=100,
    )

    behavioural_incidents: int = Field(
        default=0,
        ge=0,
    )


class StudentIntelligenceRequest(BaseModel):
    student_id: str = "STU78291"
    student_name: str = "Student"

    grade: Optional[str] = None
    school_name: Optional[str] = None
    district: Optional[str] = None

    attendance_rate: float = Field(
        ...,
        ge=0,
        le=100,
    )

    average_test_score: float = Field(
        ...,
        ge=0,
        le=100,
    )

    household_income: float = Field(
        ...,
        ge=0,
    )

    distance_to_school: float = Field(
        ...,
        ge=0,
    )

    internet_access: bool

    behavioural_incidents: int = Field(
        default=0,
        ge=0,
    )

    history: List[HistoryPoint] = []
