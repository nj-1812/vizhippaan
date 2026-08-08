from fastapi import APIRouter, HTTPException

from app.schemas.digital_twin import (
    DigitalTwinRequest,
    DigitalTwinResponse,
)

from app.services.digital_twin_service import (
    digital_twin_service,
)


router = APIRouter(
    prefix="/features",
    tags=["AI Student Digital Twin"],
)


@router.post(
    "/digital-twin",
    response_model=DigitalTwinResponse,
)
async def digital_twin(
    payload: DigitalTwinRequest,
):
    """
    Generate a CatBoost-powered AI Student Digital Twin.
    """

    try:
        return digital_twin_service.generate(payload)

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="VIZHIPPAAN model file could not be found.",
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Digital Twin generation failed: {str(exc)}",
        ) from exc
