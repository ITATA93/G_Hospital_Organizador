# API Documentation

## Overview

The Antigravity Workspace API provides endpoints for managing and executing AI agents.

**Base URL:** `http://localhost:8000`

## Authentication

Currently, the API does not require authentication. In production, implement appropriate authentication mechanisms.

---

## Endpoints

### Health Check

#### `GET /health`

Check application health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### Agents

#### `GET /api/v1/agents`

List all available agents.

**Response:**
```json
[
  {
    "name": "code-analyst",
    "description": "Analyzes code structure and patterns",
    "category": "analysis",
    "available": true
  },
  {
    "name": "doc-writer",
    "description": "Generates documentation from code",
    "category": "documentation",
    "available": true
  }
]
```

---

#### `GET /api/v1/agents/{agent_name}`

Get information about a specific agent.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| agent_name | string | Name of the agent |

**Response (200):**
```json
{
  "name": "code-analyst",
  "description": "Analyzes code structure and patterns",
  "category": "analysis",
  "available": true
}
```

**Response (404):**
```json
{
  "detail": "Agent 'nonexistent' not found"
}
```

---

#### `POST /api/v1/agents/{agent_name}/execute`

Execute an agent with the given input.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| agent_name | string | Name of the agent to execute |

**Request Body:**
```json
{
  "input": "Analyze this code for best practices",
  "context": {
    "language": "python",
    "framework": "fastapi"
  }
}
```

**Response (200):**
```json
{
  "agent": "code-analyst",
  "output": "Analysis results...",
  "metadata": {
    "input_length": 35,
    "context_provided": true
  }
}
```

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Interactive Documentation

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
