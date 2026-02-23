"""Agent service for managing and executing agents."""

from pathlib import Path
from typing import Any

import structlog

from src.models.schemas import AgentExecuteResponse, AgentInfo

logger = structlog.get_logger()


class AgentService:
    """Service for managing AI agents."""

    def __init__(self) -> None:
        """Initialize the agent service."""
        self._agents: dict[str, AgentInfo] = {}
        self._load_agents()

    def _load_agents(self) -> None:
        """Load available agents from configuration."""
        agents_dir = Path(".gemini/agents")
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.toml"):
                agent_name = agent_file.stem
                self._agents[agent_name] = AgentInfo(
                    name=agent_name,
                    description=f"Agent loaded from {agent_file.name}",
                    category="gemini",
                    available=True,
                )
                logger.info("agent_loaded", agent=agent_name)

        # Add default agents if none found
        if not self._agents:
            default_agents = [
                AgentInfo(
                    name="code-analyst",
                    description="Analyzes code structure and patterns",
                    category="analysis",
                    available=True,
                ),
                AgentInfo(
                    name="doc-writer",
                    description="Generates documentation from code",
                    category="documentation",
                    available=True,
                ),
                AgentInfo(
                    name="test-writer",
                    description="Generates test cases for code",
                    category="testing",
                    available=True,
                ),
            ]
            for agent in default_agents:
                self._agents[agent.name] = agent

    def list_agents(self) -> list[AgentInfo]:
        """Get list of all available agents."""
        return list(self._agents.values())

    def get_agent(self, name: str) -> AgentInfo | None:
        """Get agent by name."""
        return self._agents.get(name)

    async def execute_agent(
        self,
        agent_name: str,
        input_text: str,
        context: dict[str, Any] | None = None,
    ) -> AgentExecuteResponse:
        """Execute an agent with the given input."""
        logger.info(
            "agent_execution_started",
            agent=agent_name,
            input_length=len(input_text),
            has_context=context is not None,
        )

        # Placeholder for actual agent execution
        # In a real implementation, this would call the actual agent
        output = f"Agent '{agent_name}' processed: {input_text[:100]}..."

        logger.info("agent_execution_completed", agent=agent_name)

        return AgentExecuteResponse(
            agent=agent_name,
            output=output,
            metadata={
                "input_length": len(input_text),
                "context_provided": context is not None,
            },
        )
