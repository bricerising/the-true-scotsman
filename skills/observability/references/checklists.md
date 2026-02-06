# Observability Checklists

Use these as “minimum viable observability” for enterprise web apps.

## Boundary Instrumentation Checklist

For each external boundary (HTTP handler, gRPC method, job run, message consume, WS action):

- Name the decision this telemetry supports (what action it should trigger).
- Define the operation name (`op`) using a stable template (route template / RPC method / job name).
- Create or continue a trace context; start a span for the unit of work.
- Add child spans around downstream calls (DB/cache/HTTP/gRPC).
- Record boundary RED metrics (rate, errors, duration).
- Log at the boundary (especially on errors) with correlation IDs and stable fields.
- Ensure spans always end (timeouts/cancellation paths included).

## Logging Checklist

- Use structured JSON logs with stable keys.
- Include correlation IDs: `traceId` and `spanId` (or `requestId` if that’s your primary correlation key).
- Emit one high-quality error log per request at the edge (avoid duplicative logs in every layer).
- Avoid secrets/credentials; define what identifiers are safe to log.
- Prefer a structured error model:
  - `err.type` / `err.code` (stable signifier)
  - `err.message` (human readable)
  - `err.stack` (unknown/unexpected failures only, or behind a policy)

## Tracing Checklist

- Root spans start at the edge (ingress) and propagate to all internal calls.
- Use consistent span naming:
  - `HTTP <METHOD> <ROUTE_TEMPLATE>`
  - `grpc <Service>/<Method>`
  - `db <OP>` or `redis <CMD>`
- Keep span attributes low-cardinality; never include raw request bodies.
- Attach outcome fields (status code, error type/code, retry count).

## Metrics Checklist

- Start with boundary RED metrics:
  - `requests_total{route=...}`
  - `request_errors_total{route=..., error=...}` (bounded error codes only)
  - `request_duration_seconds_bucket{route=...}`
- Add a small set of business/domain metrics aligned to product intent.
- Ensure each metric maps to a specific decision.
- Cardinality rules:
  - Never label by `userId`, `accountId`, table IDs, UUIDs, emails, etc.
  - Prefer route templates and bounded enums.

## Measurement Ladder Checklist

- 3 leading indicators are defined (move within days).
- 3 lagging outcomes are defined (move within weeks/months).
- Instrumentation source is explicit (logs/metrics/traces/tests/event store).
- Owner, cadence, and action threshold are explicit.

## Dashboards (Minimum Set)

- **Traffic**: request rate by route/RPC.
- **Errors**: error rate by route/RPC + top error codes.
- **Latency**: p50/p95/p99 by route/RPC.
- **Dependencies**: DB/Redis request rate + duration + errors.
- **Saturation**: CPU/memory, event loop lag, thread/connection pools, queue lag.

## Alerts (Principles)

- Alert on **symptoms** (SLO burn, error rate, latency) before causes.
- Every alert should link to:
  - a dashboard (or Explore query)
  - a runbook note (“what to check next”)
  - relevant logs/traces filters (service + operation)
- Every alert should map to a specific operator decision (roll back, scale, reroute, ignore, investigate).

## Triage Flow (Fast Path)

1. Find the failing request in logs; extract `traceId` (or `requestId`).
2. Open the trace and identify the slow/error span (dependency, DB, cache, downstream service).
3. Use trace-to-metrics and service dashboards to validate whether it’s systemic.
4. Use logs filtered by `traceId` to capture the exact error semantics and context.

## Optional external reading

- Google SRE Book: “Monitoring Distributed Systems” https://sre.google/sre-book/monitoring-distributed-systems/
- OpenTelemetry documentation https://opentelemetry.io/docs/
- OpenTelemetry Semantic Conventions https://opentelemetry.io/docs/specs/semconv/
