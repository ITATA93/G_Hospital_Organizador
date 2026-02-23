"""Shared pytest fixtures and configuration."""

from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.main import app


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
