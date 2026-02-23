# Metrics Standards

## Overview

This document defines the metrics to collect and monitor for the Antigravity Workspace.

---

## Metric Types

### Counter
Cumulative values that only increase (or reset to zero).
- Requests count
- Errors count
- Agent executions

### Gauge
Point-in-time values that can go up or down.
- Active connections
- Memory usage
- Queue depth

### Histogram
Distribution of values over time.
- Request latency
- Payload size
- Execution duration

---

## Application Metrics

### HTTP Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| http_requests_total | Counter | method, path, status | Total HTTP requests |
| http_request_duration_seconds | Histogram | method, path | Request latency |
| http_requests_in_progress | Gauge | method | Active requests |

### Agent Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| agent_executions_total | Counter | agent, status | Total agent executions |
| agent_execution_duration_seconds | Histogram | agent | Execution time |
| agent_active_executions | Gauge | agent | Currently running |
| agent_errors_total | Counter | agent, error_type | Agent errors |

### Business Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| analysis_completed_total | Counter | type | Completed analyses |
| code_generated_lines_total | Counter | language | Lines of code generated |
| documents_generated_total | Counter | format | Documents created |

---

## Infrastructure Metrics

### Resource Usage

| Metric | Type | Description |
|--------|------|-------------|
| process_cpu_seconds_total | Counter | CPU time used |
| process_memory_bytes | Gauge | Memory usage |
| process_open_fds | Gauge | Open file descriptors |

### Database Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| db_connections_active | Gauge | pool | Active connections |
| db_query_duration_seconds | Histogram | operation | Query latency |
| db_errors_total | Counter | operation | Database errors |

---

## SLI/SLO Definitions

### Service Level Indicators (SLI)

| SLI | Definition | Measurement |
|-----|------------|-------------|
| Availability | Service is responding | Successful health checks / Total checks |
| Latency | Response time | P95 request duration |
| Error Rate | Requests without errors | Successful requests / Total requests |
| Throughput | Processing capacity | Requests per second |

### Service Level Objectives (SLO)

| SLO | Target | Measurement Window |
|-----|--------|-------------------|
| Availability | 99.9% | Monthly |
| P95 Latency | < 500ms | Daily |
| Error Rate | < 0.1% | Daily |
| Agent Success | > 95% | Weekly |

---

## Dashboards

### Overview Dashboard

```
+-----------------------------------+
|  Request Rate    |  Error Rate    |
|  [sparkline]     |  [sparkline]   |
+-----------------------------------+
|  P50 Latency     |  P95 Latency   |
|  45ms            |  120ms         |
+-----------------------------------+
|  Active Agents   |  Queue Depth   |
|  3               |  12            |
+-----------------------------------+
```

### Agent Performance Dashboard

```
+-----------------------------------+
|  Executions/min by Agent          |
|  [stacked bar chart]              |
+-----------------------------------+
|  Success Rate by Agent            |
|  [line chart over time]           |
+-----------------------------------+
|  Duration Distribution            |
|  [histogram]                      |
+-----------------------------------+
```

---

## Implementation

### Prometheus Integration

```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"]
)

AGENT_EXECUTIONS = Counter(
    "agent_executions_total",
    "Total agent executions",
    ["agent", "status"]
)
```

### Recording Metrics

```python
import time

def execute_agent(name: str, input: str):
    start = time.time()
    try:
        result = agent.execute(input)
        AGENT_EXECUTIONS.labels(agent=name, status="success").inc()
        return result
    except Exception as e:
        AGENT_EXECUTIONS.labels(agent=name, status="error").inc()
        raise
    finally:
        duration = time.time() - start
        AGENT_DURATION.labels(agent=name).observe(duration)
```

---

## Alerting Rules

```yaml
groups:
  - name: antigravity
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected

      - alert: SlowResponses
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: P95 latency above 1 second
```
