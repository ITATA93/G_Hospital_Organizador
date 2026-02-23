# Architecture: Middleware

This system uses FastAPI's middleware stack to handle cross-cutting concerns.

## 1. Request ID (Traceability)
*   **Class**: `RequestIDMiddleware`
*   **File**: `src/main.py`
*   **Function**:
    *   Generates a UUID4 for every incoming request.
    *   Attaches it to `request.state.request_id`.
    *   Returns it in the header `X-Request-ID`.
*   **Use Case**: Debugging distributed systems. Search logs by this ID to trace a full transaction.

## 2. CORS (Cross-Origin Resource Sharing)
*   **Standard**: `CORSMiddleware`
*   **Configuration**:
    *   **Development**: Allows `["*"]` (Everywhere).
    *   **Production**: Restricted to `settings.frontend_url`.
*   **Security Note**: Never deploy with `["*"]` to production unless it's a public API.
