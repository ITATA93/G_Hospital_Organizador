"""Unit tests for models."""

from datetime import datetime, timezone

from src.models.schemas import (
    AgentExecuteRequest,
    AgentExecuteResponse,
    AgentInfo,
    HealthResponse,
)


class TestHealthResponse:
    """Tests for HealthResponse model."""

    def test_create_health_response(self) -> None:
        """Test creating a health response."""
        response = HealthResponse(
            status="healthy",
            version="1.0.0",
            timestamp=datetime.now(timezone.utc),
        )

        assert response.status == "healthy"
        assert response.version == "1.0.0"
        assert isinstance(response.timestamp, datetime)


class TestAgentInfo:
    """Tests for AgentInfo model."""

    def test_create_agent_info(self) -> None:
        """Test creating agent info."""
        agent = AgentInfo(
            name="test-agent",
            description="A test agent",
            category="testing",
            available=True,
        )

        assert agent.name == "test-agent"
        assert agent.available is True

    def test_agent_info_default_available(self) -> None:
        """Test that available defaults to True."""
        agent = AgentInfo(
            name="test",
            description="Test",
            category="test",
        )

        assert agent.available is True


class TestAgentExecuteRequest:
    """Tests for AgentExecuteRequest model."""

    def test_create_request_without_context(self) -> None:
        """Test creating a request without context."""
        request = AgentExecuteRequest(input="Test input")

        assert request.input == "Test input"
        assert request.context is None

    def test_create_request_with_context(self) -> None:
        """Test creating a request with context."""
        request = AgentExecuteRequest(
            input="Test input",
            context={"key": "value"},
        )

        assert request.context == {"key": "value"}


class TestAgentExecuteResponse:
    """Tests for AgentExecuteResponse model."""

    def test_create_response(self) -> None:
        """Test creating an execution response."""
        response = AgentExecuteResponse(
            agent="test-agent",
            output="Test output",
            metadata={"duration_ms": 100},
        )

        assert response.agent == "test-agent"
        assert response.output == "Test output"
        assert response.metadata["duration_ms"] == 100
