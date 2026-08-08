from typing import List, Optional

from pydantic import BaseModel, Field


# ============================================================
# HISTORICAL SNAPSHOT
# ============================================================

class HistoryPoint(BaseModel):
    period: str = Field(
        ...,
        description="Label for the historical period, e.g. Term 1",
    )

    attendance_rate: float = Field(
        ...,
        ge=0,
        le=100,
        description="Attendance percentage for this period",
    )

    average_test_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Average academic score for this period",
    )

    behavioural_incidents: int = Field(
        default=0,
        ge=0,
        description="Behavioural incidents recorded in this period",
    )


# ============================================================
# MAIN STUDENT INTELLIGENCE REQUEST
# ============================================================

class StudentIntelligenceRequest(BaseModel):
    student_id: str = Field(
        default="STU78291",
        description="Unique student identifier",
    )

    student_name: str = Field(
        default="Student",
        description="Student display name",
    )

    grade: Optional[str] = Field(
        default=None,
        description="Current grade/class",
    )

    school_name: Optional[str] = Field(
        default=None,
        description="School name",
    )

    district: Optional[str] = Field(
        default=None,
        description="District name",
    )

    attendance_rate: float = Field(
        ...,
        ge=0,
        le=100,
        description="Current attendance percentage",
    )

    average_test_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Current average academic score",
    )

    household_income: float = Field(
        ...,
        ge=0,
        description="Household income value used by the model",
    )

    distance_to_school: float = Field(
        ...,
        ge=0,
        description="Distance from home to school in kilometres",
    )

    internet_access: bool = Field(
        ...,
        description="Whether reliable internet access is available",
    )

    behavioural_incidents: int = Field(
        default=0,
        ge=0,
        description="Current recorded behavioural incidents",
    )

    history: List[HistoryPoint] = Field(
        default_factory=list,
        description="Historical student snapshots used for journey and trend analysis",
    )


# ============================================================
# API EXAMPLE
# ============================================================

class Config:
    json_schema_extra = {
        "example": {
            "student_id": "STU78291",
            "student_name": "Rohit Kumar",
            "grade": "8",
            "school_name": "Government Middle School",
            "district": "Virudhunagar",
            "attendance_rate": 61,
            "average_test_score": 53,
            "household_income": 18000,
            "distance_to_school": 7,
            "internet_access": False,
            "behavioural_incidents": 2,
            "history": [
                {
                    "period": "Term 1",
                    "attendance_rate": 78,
                    "average_test_score": 67,
                    "behavioural_incidents": 0,
                },
                {
                    "period": "Term 2",
                    "attendance_rate": 71,
                    "average_test_score": 61,
                    "behavioural_incidents": 1,
                },
                {
                    "period": "Term 3",
                    "attendance_rate": 65,
                    "average_test_score": 57,
                    "behavioural_incidents": 1,
                },
            ],
        }
    }
