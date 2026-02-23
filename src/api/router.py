"""Main API router that aggregates all endpoint modules."""

from fastapi import APIRouter

from src.api.agents import router as agents_router
from src.api.health import router as health_router

api_router = APIRouter()

# Include sub-routers
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(agents_router, prefix="/api/v1", tags=["Agents"])
