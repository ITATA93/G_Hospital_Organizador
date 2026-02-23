"""Unit tests for services."""

import pytest

from src.models.schemas import AgentInfo
from src.services.agent_service import AgentService


class TestAgentService:
    """Tests for AgentService."""

    def test_list_agents_returns_list(self) -> None:
        """Test that list_agents returns a list of agents."""
        service = AgentService()
        agents = service.list_agents()

        assert isinstance(agents, list)
        assert len(agents) > 0
        assert all(isinstance(a, AgentInfo) for a in agents)

    def test_get_agent_existing(self) -> None:
        """Test getting an existing agent."""
        service = AgentService()
        agents = service.list_agents()
        first_agent = agents[0]

        result = service.get_agent(first_agent.name)

        assert result is not None
        assert result.name == first_agent.name

    def test_get_agent_nonexistent(self) -> None:
        """Test getting a non-existent agent returns None."""
        service = AgentService()

        result = service.get_agent("nonexistent-agent")

        assert result is None

    @pytest.mark.asyncio
    async def test_execute_agent(self) -> None:
        """Test agent execution."""
        service = AgentService()
        agents = service.list_agents()
        first_agent = agents[0]

        result = await service.execute_agent(
            first_agent.name,
            "Test input",
            {"key": "value"},
        )

        assert result.agent == first_agent.name
        assert len(result.output) > 0
        assert "input_length" in result.metadata
