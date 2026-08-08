from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.journey_timeline_service import (
    journey_timeline_service,
)


router = APIRouter(
    prefix="/student-intelligence",
    tags=["Student Intelligence"],
)


class JourneyTimelineRequest(BaseModel):
    student_id: str = Field(
        ...,
        min_length=1,
        examples=["STU-1001"],
    )

    attendance_rate: float = Field(
        ...,
        ge=0,
        le=100,
        examples=[72.5],
    )

    average_test_score: float = Field(
        ...,
        ge=0,
        le=100,
        examples=[58.0],
    )

    behavioural_incidents: int = Field(
        default=0,
        ge=0,
        examples=[2],
    )

    household_income: float = Field(
        default=150000,
        ge=0,
        examples=[150000],
    )

    distance_to_school: float = Field(
        default=5,
        ge=0,
        examples=[7.5],
    )

    internet_access: bool = Field(
        default=True,
        examples=[False],
    )


@router.post("/journey-timeline")
def get_student_journey_timeline(
    payload: JourneyTimelineRequest,
):
    """
    Generate the Student Journey Timeline.

    Returns chronological student intelligence events including
    attendance, academic performance, behaviour, accessibility,
    socioeconomic indicators and the latest risk assessment.
    """

    try:
        return journey_timeline_service.build_timeline(
            student_id=payload.student_id,
            attendance_rate=payload.attendance_rate,
            average_test_score=payload.average_test_score,
            behavioural_incidents=payload.behavioural_incidents,
            household_income=payload.household_income,
            distance_to_school=payload.distance_to_school,
            internet_access=payload.internet_access,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate student journey timeline: {exc}",
        ) from exc
