"""Pydantic schemas for API request/response models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Health status")
    version: str = Field(..., description="Application version")
    timestamp: datetime = Field(..., description="Current server timestamp")


class AgentInfo(BaseModel):
    """Agent information model."""

    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    category: str = Field(..., description="Agent category")
    available: bool = Field(True, description="Whether agent is available")


class AgentExecuteRequest(BaseModel):
    """Request model for agent execution."""

    input: str = Field(..., description="Input for the agent")
    context: dict[str, Any] | None = Field(None, description="Optional context")


class AgentExecuteResponse(BaseModel):
    """Response model for agent execution."""

    agent: str = Field(..., description="Agent that processed the request")
    output: str = Field(..., description="Agent output")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Execution metadata")
