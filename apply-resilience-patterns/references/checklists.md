# Resilience Checklists

Enterprise web apps run in “partial failure” by default. Use these checklists to keep failures bounded and predictable.

## Timeout Checklist

- Every outbound call has a timeout (HTTP client, gRPC client, DB, cache).
- Timeouts participate in cancellation (propagate `AbortSignal` or gRPC deadline).
- Use a per-request “time budget”:
  - total time across retries must fit inside the budget
  - budget includes downstream latency + backoff sleeps
- Choose timeouts intentionally:
  - too short → false timeouts → retry storms
  - too long → request pileups → resource exhaustion

## Retry Checklist

- Decide what is retryable:
  - transient network errors
  - timeouts (careful: may have succeeded server-side)
  - 429/503 (if server indicates “try later”)
- Decide what is not retryable:
  - validation errors
  - auth/permission errors
  - domain/business rejections
- Backoff policy:
  - exponential backoff + jitter
  - cap delay and cap attempts
  - stop early if request budget is exhausted
- Record observability:
  - retry count as span attribute and log field
  - metrics for retries and retry-exhausted failures

## Idempotency Checklist

If there are retries, you must have idempotency.

- For HTTP:
  - Use idempotency keys for unsafe endpoints (`POST`/`PATCH` that change state).
  - Store key → result mapping (or key → “applied”) with TTL.
  - Define key scope (per user? per tenant?).
- For events/messages:
  - Assume duplicates and replays; dedupe by message ID and/or (aggregateId, version).
  - Ensure side effects are applied once (or are commutative/compensatable).
- Define semantics:
  - “same key returns same result” vs “same key is a no-op”

## Circuit Breaker Checklist

- Decide what counts as failure (timeouts, 5xx, specific error codes).
- Decide thresholds:
  - minimum requests window
  - failure rate threshold
  - open duration (cooldown)
  - half-open probe count
- Behavior when open:
  - fail fast with a stable error
  - optional fallback (cached/stale/partial) if acceptable
- Observability:
  - metrics for breaker state and transitions
  - logs only on transitions (open/half-open/close)

## Bulkhead / Concurrency Limit Checklist

- Identify resource pools you need to protect:
  - DB connections
  - Redis connections
  - outbound HTTP slots per dependency
  - CPU-heavy work
- Prefer per-dependency limits to avoid one hotspot starving everything.
- Decide queueing vs rejecting:
  - queueing increases tail latency
  - rejecting fails fast and protects the system
- Expose metrics:
  - queue depth (if queued)
  - rejected count

## Redis Streams Head-of-Line Blocking (Common Gotcha)

If you use Redis Streams with blocking reads (`XREADGROUP`/`XREAD` with `BLOCK`):

- Do **not** share the same Redis connection/client for:
  - blocking reads (stream consumption), and
  - “normal” commands used by request handlers.
- Symptom: unrelated commands (e.g. `GET`, `HSET`, `INCR`, `XADD`) show latency spikes around the `BLOCK` interval.
- Fix: use a dedicated Redis client/connection for blocking operations (duplicate the client or use a separate pool).

## Load Shedding / Rate Limiting Checklist

- Enforce at ingress (gateway/API edge) before doing expensive work.
- Separate limits for different classes of work (chat vs gameplay vs heavy reports).
- Provide stable “overloaded” errors (429/503) and include retry guidance.

## Failure-Mode Smoke Test Checklist

Before considering a change “done”, prove you can debug it:

1. Simulate dependency timeout or 5xx (local docker, stub server, or forced failure flag).
2. Confirm:
   - requests fail within the budget
   - retries happen when expected and stop when expected
   - idempotency prevents double-apply
   - logs include correlation IDs
   - traces show retry attempts and downstream spans
