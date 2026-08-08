from fastapi import (
    APIRouter,
    HTTPException,
)

from app.schemas.digital_twin import (
    DigitalTwinRequest,
    DigitalTwinResponse,
)

from app.services.digital_twin_service import (
    digital_twin_service,
)


router = APIRouter(
    prefix="/api/v1/features",
    tags=["AI Student Digital Twin"],
)


@router.post(
    "/digital-twin",
    response_model=DigitalTwinResponse,
)
async def digital_twin(
    payload: DigitalTwinRequest,
):
    try:
        return (
            digital_twin_service.generate(
                payload
            )
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "VIZHIPPAAN model file is unavailable."
            ),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Digital Twin generation failed: "
                f"{str(exc)}"
            ),
        ) from exc
