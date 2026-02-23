"""Health check endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter

from src.config import get_settings
from src.models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check application health status."""
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.now(timezone.utc),
    )
