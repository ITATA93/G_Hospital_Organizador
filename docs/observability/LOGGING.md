# Logging Standards

## Overview

This document defines logging standards for the Antigravity Workspace.

---

## Log Format

### JSON Structure (Production)

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "INFO",
  "logger": "src.services.agent_service",
  "message": "agent_execution_completed",
  "agent": "code-analyst",
  "duration_ms": 1234,
  "request_id": "abc-123-def",
  "user_id": "user_001"
}
```

### Console Format (Development)

```
2024-01-15 10:30:00 [INFO] agent_execution_completed agent=code-analyst duration_ms=1234
```

---

## Log Levels

| Level | Usage | Examples |
|-------|-------|----------|
| DEBUG | Detailed debugging info | Variable values, function entry/exit |
| INFO | Normal operations | Requests, completions, state changes |
| WARNING | Potential issues | Deprecated usage, performance warnings |
| ERROR | Errors that don't stop execution | Failed validations, recoverable errors |
| CRITICAL | System failures | Database down, service unavailable |

### Level Guidelines

```python
# DEBUG - Detailed information for debugging
logger.debug("processing_item", item_id=item.id, state=item.state)

# INFO - Normal operational events
logger.info("agent_execution_started", agent=name, input_length=len(input))

# WARNING - Potential issues
logger.warning("rate_limit_approaching", current=90, limit=100)

# ERROR - Errors that need attention
logger.error("agent_execution_failed", agent=name, error=str(e))

# CRITICAL - System failures
logger.critical("database_connection_lost", host=db_host)
```

---

## Structured Fields

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| timestamp | ISO 8601 | Event timestamp |
| level | string | Log level |
| logger | string | Logger name/module |
| message | string | Event identifier |

### Contextual Fields

| Field | Type | Description |
|-------|------|-------------|
| request_id | string | Unique request identifier |
| user_id | string | User identifier |
| agent | string | Agent name |
| duration_ms | number | Operation duration |

### Error Fields

| Field | Type | Description |
|-------|------|-------------|
| error | string | Error message |
| error_type | string | Error class name |
| stack_trace | string | Full stack trace |

---

## Implementation

### Logger Configuration

```python
import structlog

def setup_logging(level: str, format_type: str) -> None:
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if format_type == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
    )
```

### Context Propagation

```python
from structlog.contextvars import bind_contextvars

# Bind context for all subsequent logs
bind_contextvars(
    request_id=request.headers.get("X-Request-ID"),
    user_id=current_user.id,
)

# All logs now include request_id and user_id
logger.info("operation_started")
```

---

## What to Log

### Always Log

- Request start/end with timing
- Authentication events
- Agent executions
- Errors and exceptions
- Security events
- Configuration changes

### Never Log

- Passwords or credentials
- Personal Identifiable Information (PII)
- API keys or tokens
- Credit card numbers
- Session tokens

### Log Sanitization

```python
SENSITIVE_PATTERNS = [
    r"password[\"']?\s*[:=]\s*[\"']?[^\"'\s]+",
    r"api[_-]?key[\"']?\s*[:=]\s*[\"']?[^\"'\s]+",
    r"token[\"']?\s*[:=]\s*[\"']?[^\"'\s]+",
]

def sanitize_log(message: str) -> str:
    for pattern in SENSITIVE_PATTERNS:
        message = re.sub(pattern, "[REDACTED]", message, flags=re.I)
    return message
```

---

## Retention

| Environment | Retention |
|-------------|-----------|
| Development | 7 days |
| Staging | 30 days |
| Production | 90 days |

---

## Alerting

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Error rate | > 1% | > 5% |
| P95 latency | > 5s | > 10s |
| Failed agents | > 3/hour | > 10/hour |
