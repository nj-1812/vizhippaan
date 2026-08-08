from fastapi import (
    APIRouter,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)

from app.schemas.digital_twin import (
    StudentTwinRequest,
    StudentTwinResponse,
)

from app.services.digital_twin_service import (
    digital_twin_service,
)


router = APIRouter(
    prefix="/api/v1/features",
    tags=["AI Student Digital Twin"],
)


# =============================================================
# NORMAL REAL-TIME REQUEST
# =============================================================

@router.post(
    "/digital-twin",
    response_model=StudentTwinResponse,
)
async def generate_digital_twin(
    payload: StudentTwinRequest,
):
    """
    Generate the latest AI Student Digital Twin
    using the currently supplied student snapshot.
    """

    try:
        return digital_twin_service.generate(
            payload
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Digital Twin generation failed: "
                f"{str(exc)}"
            ),
        ) from exc


# =============================================================
# LIVE WEBSOCKET DIGITAL TWIN
# =============================================================

@router.websocket(
    "/digital-twin/live/{student_id}"
)
async def live_digital_twin(
    websocket: WebSocket,
    student_id: str,
):

    await websocket.accept()

    try:

        # Initial connection acknowledgement

        await websocket.send_json({
            "type":
                "connection",

            "status":
                "connected",

            "student_id":
                student_id,

            "message":
                "VIZHIPPAAN Digital Twin live stream connected",
        })

        while True:

            # Frontend sends updated attendance / marks /
            # behaviour / etc.

            raw_data = (
                await websocket.receive_json()
            )

            raw_data[
                "student_id"
            ] = student_id

            payload = StudentTwinRequest(
                **raw_data
            )

            result = (
                digital_twin_service.generate(
                    payload
                )
            )

            await websocket.send_json({
                "type":
                    "digital_twin_update",

                "data":
                    result,
            })

    except WebSocketDisconnect:
        print(
            f"Digital Twin websocket disconnected: "
            f"{student_id}"
        )

    except Exception as exc:

        try:
            await websocket.send_json({
                "type":
                    "error",

                "message":
                    str(exc),
            })

        except Exception:
            pass

        await websocket.close()
