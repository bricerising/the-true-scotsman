# Boundary Wrappers (“Golden Path” Primitives)

Use boundary wrappers to make cross-cutting behavior consistent across services without copying code.

This guide focuses on wrappers around **I/O boundaries**:

- inbound: HTTP/gRPC handlers, jobs/consumers
- outbound: HTTP/gRPC/DB/cache/SDK clients

## What A Boundary Wrapper Must Standardize

Every wrapper should make these contracts explicit and boring:

### 1) Error envelope (stable semantics)

- Define a small set of **expected** error categories (typed errors / error codes).
- Convert `unknown` failures into a stable “unexpected” category at the boundary.
- Preserve consumer-visible semantics (don’t “helpfully” change response shapes).
- Log once at the boundary with enough context; avoid duplicate logs in every layer.

### 2) Retry + idempotency policy (only when safe)

- Default: **no retries** unless you can prove they are safe.
- If you retry:
  - classify retryable vs non-retryable failures (timeouts, 429/503, connection resets)
  - bound retries by **attempt count** and **time budget**
  - use backoff + jitter
  - require an **idempotency key** (or dedupe key) when the operation is not inherently idempotent
- For at-least-once consumers/jobs, idempotency/dedupe is mandatory.

### 3) Telemetry field contract (correlation)

- Logs/traces/metrics must correlate via stable IDs/fields.
- Prefer low-cardinality labels for metrics:
  - route templates / RPC method names
  - bounded enums (error codes, outcome)
- Never use unbounded IDs (user IDs, order IDs, request IDs) as metric labels.

Recommended fields (where applicable):

- `op`: operation name (route template, `grpc Service/Method`, job name, message type)
- `traceId`, `spanId`: trace correlation
- `requestId`: request correlation (may equal `traceId`)
- `attempt`: retry attempt number
- `durationMs` (logs) and histogram metrics (preferred)
- `err.code` / `err.type`: stable error classification

## Wrapper Shapes

### Inbound handlers (HTTP/gRPC)

Goal: standardize `decode → call → map response` plus time budgets + telemetry + error mapping.

Suggested responsibilities:

- decode/validate external input (`unknown` → typed)
- start a root span and attach `op`
- enforce time budget (deadline / `AbortSignal`)
- call domain/service function
- map expected errors to stable error envelope / status codes
- emit RED metrics for the boundary

See `references/templates.md` for a handler wrapper skeleton.

### Outbound clients (HTTP/gRPC/SDK)

Goal: standardize timeouts, cancellation, retries (when safe), and error mapping across call sites.

Suggested responsibilities:

- accept `op`, a time budget, and an `AbortSignal`/deadline
- map library-specific errors into stable error categories
- apply retries only via an explicit retry policy
- emit child spans + consistent log fields

### Jobs and async consumers

Goal: make “run one unit of work” consistent:

- start a root span per unit of work (message/job run)
- decode/validate payload at the boundary
- enforce time budgets and cancellation
- make idempotency/dedupe explicit (inbox/outbox patterns)
- acknowledge/commit only after durable side effects succeed

## Design Checklist (Quick)

- Operation naming is explicit (`op` passed in; no reflection magic).
- Time budget is explicit (deadline / `AbortSignal`) and propagated.
- Errors are typed and mapped at the boundary; `unknown` is normalized.
- Retries are bounded and paired with idempotency/dedupe (when applicable).
- Telemetry field contract is stable and low-cardinality.
- Wrapper is small and composable (interceptors/decorators), not a “mega framework”.
- Tests cover: happy path, one expected failure, one timeout/cancellation, retry classification (if used).

## Related Skills

- `resilience` (timeouts, retries, idempotency)
- `observability` (field contracts + correlation)
- `typescript` (typed errors, lifetimes, boundaries)
