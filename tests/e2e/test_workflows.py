"""End-to-end workflow tests."""

import pytest
from fastapi.testclient import TestClient


class TestAgentWorkflow:
    """E2E tests for complete agent workflows."""

    @pytest.mark.e2e
    def test_complete_agent_workflow(self, client: TestClient) -> None:
        """Test a complete workflow: list -> get -> execute."""
        # Step 1: List available agents
        list_response = client.get("/api/v1/agents")
        assert list_response.status_code == 200
        agents = list_response.json()
        assert len(agents) > 0

        # Step 2: Get details of first agent
        agent_name = agents[0]["name"]
        get_response = client.get(f"/api/v1/agents/{agent_name}")
        assert get_response.status_code == 200
        agent = get_response.json()
        assert agent["available"] is True

        # Step 3: Execute the agent
        execute_response = client.post(
            f"/api/v1/agents/{agent_name}/execute",
            json={
                "input": "Analyze this sample code for potential improvements",
                "context": {"language": "python"},
            },
        )
        assert execute_response.status_code == 200
        result = execute_response.json()
        assert result["agent"] == agent_name
        assert len(result["output"]) > 0

    @pytest.mark.e2e
    def test_health_check_available(self, client: TestClient) -> None:
        """Test that health check is always available."""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
