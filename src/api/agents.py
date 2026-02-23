"""Agent management endpoints."""

from fastapi import APIRouter, HTTPException

from src.models.schemas import AgentExecuteRequest, AgentExecuteResponse, AgentInfo
from src.services.agent_service import AgentService

router = APIRouter()
agent_service = AgentService()


@router.get("/agents", response_model=list[AgentInfo])
async def list_agents() -> list[AgentInfo]:
    """List all available agents."""
    return agent_service.list_agents()


@router.get("/agents/{agent_name}", response_model=AgentInfo)
async def get_agent(agent_name: str) -> AgentInfo:
    """Get information about a specific agent."""
    agent = agent_service.get_agent(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    return agent


@router.post("/agents/{agent_name}/execute", response_model=AgentExecuteResponse)
async def execute_agent(agent_name: str, request: AgentExecuteRequest) -> AgentExecuteResponse:
    """Execute an agent with the given input."""
    agent = agent_service.get_agent(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    result = await agent_service.execute_agent(agent_name, request.input, request.context)
    return result
