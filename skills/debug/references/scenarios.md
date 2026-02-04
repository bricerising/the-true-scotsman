# Scenario Checklists

Use these as a guide to keep triage systematic and fast.

## HTTP: error spike (5xx) or latency regression

1. Identify the operation:
   - route template (not raw URL)
   - status codes (4xx vs 5xx vs timeouts)
2. Find 1–3 exemplar requests in logs:
   - capture `traceId` / `requestId`, `op`, and top-level error envelope
3. Use traces to locate the “first failure”:
   - dependency call timing out?
   - retry amplification?
   - DB span slow/error?
4. Use metrics to confirm scope:
   - request rate change (traffic spike?)
   - error rate and p95 latency by route (if available)
   - saturation signals (CPU/mem/event loop/DB connections)
5. Mitigation checklist:
   - rollback latest deploy or disable flag
   - shed load / rate limit if needed
   - scale the dependency that’s saturated
6. Fix checklist:
   - add/adjust timeouts and propagate cancellation
   - eliminate unsafe retries (or add idempotency/dedupe)
   - optimize DB query or add index (validate via span timing)

## gRPC: `DEADLINE_EXCEEDED` / slow method

1. Identify:
   - `grpc_service` + `grpc_method`
   - caller and server services
2. Logs:
   - look for `DEADLINE_EXCEEDED`, `UNAVAILABLE`, connection resets
   - confirm call deadlines/time budgets are set and propagated
3. Traces:
   - confirm client/server spans are linked (if using trace context propagation)
   - find the slowest server span and the slowest downstream span
4. Metrics:
   - error rate by `grpc_code`
   - latency p95 by method
5. Common causes:
   - missing deadline propagation
   - server threadpool/concurrency exhaustion
   - downstream dependency latency (DB/cache/HTTP)
   - retry amplification without idempotency

## Async consumer: backlog / lag / poison messages

1. Identify:
   - consumer group / worker name
   - message type / topic / stream
2. Metrics:
   - backlog depth / lag (if exported)
   - processing rate vs incoming rate
   - DLQ rate (if applicable)
3. Logs:
   - repeated failures on the same message key/ID?
   - deserialization/validation errors (input contract drift)?
   - timeouts calling downstream dependencies?
4. Traces (if you propagate context):
   - confirm each message run has a trace root span
   - look for repeated retries and long-running spans
5. Mitigation checklist:
   - pause ingestion (if possible) or slow producers
   - quarantine poison messages (DLQ) to restore throughput
   - scale consumers (only if you’re not hitting a downstream limit)
6. Fix checklist:
   - validate inputs at the consumer boundary (treat as `unknown`)
   - ensure idempotency/dedupe (at-least-once delivery is normal)
   - add per-message timeouts + cancellation

