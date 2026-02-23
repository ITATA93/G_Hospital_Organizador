"""Integration tests for API endpoints."""

from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client: TestClient) -> None:
        """Test health endpoint returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data


class TestAgentsEndpoints:
    """Tests for agent endpoints."""

    def test_list_agents(self, client: TestClient) -> None:
        """Test listing all agents."""
        response = client.get("/api/v1/agents")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_agent(self, client: TestClient) -> None:
        """Test getting a specific agent."""
        # First get list to find an agent name
        list_response = client.get("/api/v1/agents")
        agents = list_response.json()
        agent_name = agents[0]["name"]

        response = client.get(f"/api/v1/agents/{agent_name}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == agent_name

    def test_get_nonexistent_agent(self, client: TestClient) -> None:
        """Test getting a non-existent agent returns 404."""
        response = client.get("/api/v1/agents/nonexistent-agent")

        assert response.status_code == 404

    def test_execute_agent(self, client: TestClient, sample_agent_input: dict) -> None:
        """Test executing an agent."""
        # First get list to find an agent name
        list_response = client.get("/api/v1/agents")
        agents = list_response.json()
        agent_name = agents[0]["name"]

        response = client.post(
            f"/api/v1/agents/{agent_name}/execute",
            json=sample_agent_input,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["agent"] == agent_name
        assert "output" in data
