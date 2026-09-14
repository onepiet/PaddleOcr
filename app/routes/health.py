from fastapi import APIRouter
from app.schemas.ocr import HealthCheckResponse
from app.config import settings

router = APIRouter()

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(
        status="ok",
        ocr="available",
        engine="PaddleOCR",
        version="v3.7.0",
        device="gpu" if settings.USE_GPU else "cpu"
    )
