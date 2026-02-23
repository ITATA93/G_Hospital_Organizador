from typing import Any

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    tool: str
    arguments: dict[str, Any]


class AgentRequest(BaseModel):
    prompt: str
    agent_name: str
    vendor: str | None = "gemini"
    parameters: dict[str, Any] | None = None


class AgentResponse(BaseModel):
    """Standardized output schema for all agents (Finding F-05)."""

    status: str = Field(..., description="success, error, or thinking")
    content: str = Field(..., description="The main text response from the agent")
    data: dict[str, Any] | None = Field(None, description="Structured data if requested")
    tool_calls: list[ToolCall] = Field(default_factory=list, description="List of tools invoked")
    meta: dict[str, Any] = Field(
        default_factory=dict, description="Execution metadata (time, cost, model)"
    )
