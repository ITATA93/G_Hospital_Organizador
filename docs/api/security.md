# API Security

This API implements a lightweight but robust security model suitable for microservices.

## 1. API Key Authentication
*   **Method**: `APIKeyHeader`
*   **Header Name**: `X-API-Key`
*   **Logic**:
    *   Located in `src/main.py:get_api_key`.
    *   **Development**: Authentication is permissive (often bypassed or optional, depending on config).
    *   **Production**: **STRICT**. The key must match `settings.api_key`.
*   **Failure**: Returns `401 Unauthorized` if keys do not match.

## 2. Best Practices
*   Rotate keys every 90 days.
*   Do not commit API Keys to Git (use `.env`).
*   For frontend clients, prefer OAuth2 (Auth0/Cognito) over static keys. This method is primarily for Server-to-Server communication.
