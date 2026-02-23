# Distributed Tracing

## Overview

This document describes the tracing strategy for tracking AI agent decisions and request flows.

---

## Concepts

### Trace
A complete request journey through the system.

### Span
A single unit of work within a trace.

### Context
Metadata propagated across service boundaries.

---

## Trace Structure

```
Trace: user-request-abc123
│
├── Span: http-request
│   ├── method: POST
│   ├── path: /api/v1/agents/code-analyst/execute
│   └── duration: 1234ms
│
├── Span: auth-validation
│   ├── user_id: user_001
│   └── duration: 5ms
│
├── Span: agent-execution
│   ├── agent: code-analyst
│   ├── input_length: 500
│   ├── output_length: 1200
│   └── duration: 1200ms
│   │
│   ├── Span: input-validation
│   │   └── duration: 10ms
│   │
│   ├── Span: ai-model-call
│   │   ├── model: gemini-pro
│   │   ├── tokens_in: 150
│   │   ├── tokens_out: 300
│   │   └── duration: 1150ms
│   │
│   └── Span: output-validation
│       └── duration: 15ms
│
└── Span: response-serialization
    └── duration: 5ms
```

---

## AI Decision Tracing

### Decision Points

Each AI agent decision should be traced:

```python
with tracer.start_span("ai_decision") as span:
    span.set_attribute("decision.type", "code_analysis")
    span.set_attribute("decision.confidence", 0.95)
    span.set_attribute("decision.factors", json.dumps(factors))
    span.set_attribute("decision.result", result_summary)
```

### Attributes to Capture

| Attribute | Type | Description |
|-----------|------|-------------|
| decision.type | string | Type of decision made |
| decision.confidence | float | Confidence score (0-1) |
| decision.factors | string | JSON of input factors |
| decision.result | string | Summary of decision |
| decision.alternatives | string | Other considered options |

---

## Implementation

### FastAPI Integration

```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

tracer = trace.get_tracer(__name__)

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Manual span for agent execution
@app.post("/api/v1/agents/{name}/execute")
async def execute_agent(name: str, request: AgentRequest):
    with tracer.start_as_current_span("agent_execution") as span:
        span.set_attribute("agent.name", name)
        span.set_attribute("input.length", len(request.input))

        result = await agent_service.execute(name, request.input)

        span.set_attribute("output.length", len(result.output))
        span.set_attribute("execution.success", True)

        return result
```

### Context Propagation

```python
from opentelemetry.propagate import extract, inject

# Extract context from incoming request
context = extract(request.headers)

# Create span with extracted context
with tracer.start_as_current_span("process", context=context):
    # Processing...
    pass

# Inject context into outgoing request
headers = {}
inject(headers)
```

---

## Trace Sampling

### Strategies

| Strategy | Use Case |
|----------|----------|
| Always On | Development, debugging |
| Probabilistic | Production (1-10%) |
| Rate Limited | High traffic (100/s) |
| Tail-based | Capture slow/error traces |

### Configuration

```python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

# Sample 10% of traces
sampler = TraceIdRatioBased(0.1)
```

---

## Correlation

### Request ID Flow

```
[Client] --X-Request-ID--> [API] --correlation_id--> [Agent]
                                                         |
                           <--trace_id + span_id--------+
```

### Log Correlation

```python
import structlog
from opentelemetry import trace

def add_trace_context(logger, method_name, event_dict):
    span = trace.get_current_span()
    if span:
        ctx = span.get_span_context()
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    return event_dict

structlog.configure(
    processors=[
        add_trace_context,
        # ... other processors
    ]
)
```

---

## Visualization

### Trace Timeline

```
|--[http-request 1234ms]----------------------------------|
    |--[auth 5ms]--|
                    |--[agent-execution 1200ms]----------|
                       |--[validation 10ms]--|
                                              |--[ai-call 1150ms]--|
                                                                    |--[validate 15ms]--|
                                                                                         |--[serialize 5ms]--|
```

### Dependency Map

```
          +--------+
          | Client |
          +---+----+
              |
              v
          +---+----+
          |  API   |
          +---+----+
              |
     +--------+--------+
     |                 |
     v                 v
+----+----+      +-----+-----+
|  Agent  |      |  Database |
+---------+      +-----------+
```

---

## Best Practices

1. **Always propagate context** - Ensure trace context flows through all services
2. **Add meaningful attributes** - Include relevant business context
3. **Keep spans focused** - One span per logical operation
4. **Handle errors properly** - Record exceptions in spans
5. **Sample appropriately** - Balance observability with cost
