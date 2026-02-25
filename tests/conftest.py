"""Shared pytest fixtures and configuration.

Sets test environment variables BEFORE importing the application,
so that pydantic Settings never fails due to a missing API_KEY.
"""

import os
from collections.abc import AsyncGenerator

# ---------------------------------------------------------------------------
# Inject required env vars *before* any application import triggers
# Settings() validation.  This makes the test-suite self-contained:
# it will pass even without a .env file on disk.
# ---------------------------------------------------------------------------
os.environ.setdefault("API_KEY", "test-api-key-not-real")
os.environ.setdefault("APP_ENV", "development")

# Clear the lru_cache on get_settings so the test values are picked up
# even if another module already imported config.
from src.config import get_settings  # noqa: E402

get_settings.cache_clear()

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402

from src.main import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    """Create a test client for synchronous tests."""
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture
def sample_agent_input() -> dict:
    """Sample input for agent execution tests."""
    return {
        "input": "Analyze this code for best practices",
        "context": {"language": "python", "framework": "fastapi"},
    }
