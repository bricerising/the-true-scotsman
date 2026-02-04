# Shared Platform Library Checklists

## Candidate Extraction Checklist

Before moving code into the platform library:

- Used (or needed imminently) in 2+ services.
- Semantics are stable and can be named (not a one-off workaround).
- It reduces risk or complexity at a boundary (auth, RPC, config, telemetry, retries).
- It does not encode domain/business rules.

## API Design Checklist

- Inputs are typed; external data is treated as `unknown` and decoded at the edge.
- Expected failures are explicit (`Result` or tagged error variants), not free-form strings.
- Cancellation is supported (`AbortSignal` or explicit deadlines) for long-running calls.
- Timeouts are explicit (either passed in or derived from a “time budget”).
- Operation naming is explicit (no reflection-dependent metrics/log names).
- No top-level side effects: importing the module does not open sockets or read env.

## Testing Checklist

- Unit tests cover:
  - happy path
  - one failure path
  - cancellation/timeout path (when applicable)
- If the primitive wraps a boundary (gRPC/HTTP/Redis/DB), tests assert:
  - error mapping
  - retry classification (retryable vs not)
  - idempotency behavior (if retries exist)

## Observability Checklist

- Logs include correlation IDs (traceId/spanId or requestId).
- Traces span the end-to-end boundary and include child spans for downstream calls.
- Metrics avoid high-cardinality labels; route templates and bounded enums only.

## Governance Checklist (“Keep It Cohesive”)

- Prefer a few “golden path” primitives over many tiny helpers.
- Every exported API has:
  - 1–2 usage examples in docs or tests
  - a clear owner (even if informal)
- Deprecations are explicit:
  - keep old API working while migrating call sites
  - remove only after adoption and verification
