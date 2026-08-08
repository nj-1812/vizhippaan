from fastapi import (
    APIRouter,
    HTTPException,
)

from app.schemas.student_intelligence import (
    StudentIntelligenceRequest,
)

from app.services.student_intelligence_service import (
    student_intelligence_service,
)


router = APIRouter(
    prefix="/student-intelligence",
    tags=["Student Intelligence"],
)


@router.post("/digital-twin")
async def digital_twin(
    payload: StudentIntelligenceRequest,
):
    try:
        return (
            student_intelligence_service
            .digital_twin(
                payload
            )
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.post("/journey-timeline")
async def journey_timeline(
    payload: StudentIntelligenceRequest,
):
    try:
        return (
            student_intelligence_service
            .journey_timeline(
                payload
            )
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.post("/risk-explanation")
async def risk_explanation(
    payload: StudentIntelligenceRequest,
):
    try:
        return (
            student_intelligence_service
            .risk_explanation(
                payload
            )
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.post("/early-warning")
async def early_warning(
    payload: StudentIntelligenceRequest,
):
    try:
        return (
            student_intelligence_service
            .early_warning(
                payload
            )
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
