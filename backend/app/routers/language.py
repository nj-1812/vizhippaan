from fastapi import APIRouter, HTTPException

from app.services.translation_service import (
    get_supported_languages,
    is_supported_language,
)

router = APIRouter(
    prefix="/api/languages",
    tags=["Languages"],
)


@router.get("")
async def languages():
    return {
        "success": True,
        "languages": get_supported_languages()
    }


@router.get("/{language_code}")
async def validate_language(language_code: str):

    language_code = language_code.lower()

    if not is_supported_language(language_code):
        raise HTTPException(
            status_code=400,
            detail="Unsupported language"
        )

    return {
        "success": True,
        "language": language_code
    }
