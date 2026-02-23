"""FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware

from src.api.router import api_router
from src.config import get_settings
from src.utils.logger import setup_logging

settings = get_settings()

# Setup structured logging
setup_logging(settings.log_level, settings.log_format)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan events (startup/shutdown)."""
    import structlog

    logger = structlog.get_logger()
    logger.info("application_started", app=settings.app_name, version=settings.app_version)
    yield
    logger.info("application_stopped")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Multi-agent development workspace template",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Security & Middleware

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if settings.environment == "production" and api_key != settings.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key",
            )
    return api_key


# CORS middleware (F-04: Restricted origins)
origins = (
    ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000", "http://127.0.0.1:8000"]
    if settings.environment == "development"
    else [settings.frontend_url]
)

# middleware to add request ID


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


app.add_middleware(RequestIDMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)
