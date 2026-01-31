---
name: apply-resilience-patterns
description: Apply resilience patterns for enterprise services (timeouts, retries with backoff+jitter, idempotency, circuit breakers, bulkheads/concurrency limits, safe fallbacks). Use when adding/refactoring outbound calls, consumers/jobs, retry behavior, or hardening a service against partial failures and flaky dependencies.
---

# Apply Resilience Patterns

## Overview

Make I/O failures boring: set explicit timeouts, retry safely, keep operations idempotent, and prevent cascades with circuit breakers and bulkheads.

Enterprise systems fail partially (timeouts, 5xx, queue lag). Resilience patterns make those failures bounded and observable.

## Workflow

1. Identify the I/O boundary: HTTP, gRPC, DB, cache, queue/stream, third-party API.
2. Define the failure model:
   - which failures are expected/transient vs permanent
   - what “success” means under degradation (fallback? partial data? fail fast?)
3. Apply patterns in this order:
   1. **Timeouts + cancellation**
   2. **Idempotency** (especially if retries exist)
   3. **Retries with backoff + jitter** (bounded)
   4. **Circuit breaker** (when a dependency is unhealthy)
   5. **Bulkheads / concurrency limits** (to protect your own resources)
4. Add observability (retry counts, breaker state, queue lag, error codes).
5. Add consumer-visible tests for semantics; add a local smoke test for failure modes.

## Chooser (What To Use Where)

- **Inbound HTTP/gRPC**: timeouts for downstream calls; guardrails; load shedding; return stable error codes.
- **Outbound HTTP/gRPC clients**: timeouts + bounded retries + (optional) circuit breaker + concurrency limit.
- **DB/Redis**: short timeouts; limited retries (often none); concurrency limits/pools; backpressure.
- **Message consumers**: idempotency + dedupe; retry with backoff; dead-letter strategy; track lag.

## Core Patterns (Opinionated Defaults)

### Timeouts + cancellation (mandatory)

- Every outbound call has a timeout and participates in cancellation.
- Use a single “time budget” per request; don’t let retries exceed it.

### Retries (bounded, only when safe)

- Retry only for **transient** failures (timeouts, connection resets, 429/503 depending on semantics).
- Use exponential backoff + jitter to avoid synchronized retry storms.
- Cap attempts and cap total delay; consider a retry budget per request.

### Idempotency (required when retries exist)

- Never retry a non-idempotent operation unless the server-side operation is idempotent (idempotency key / dedupe).
- For message consumers, assume at-least-once delivery: handle duplicates safely.

### Circuit breaker (for flakey/unhealthy dependencies)

- Open the breaker when failure rate exceeds a threshold; fail fast for a cooldown period.
- Half-open to probe recovery; close after successful probes.
- Expose breaker state as metrics and log transitions.

### Bulkheads / concurrency limits (protect yourself)

- Limit concurrent work per dependency to avoid saturating your process.
- Prefer per-dependency limits (bulkheads) over one global limit.

## Minimal TypeScript Snippets

Backoff with jitter:

```ts
export function backoffDelayMs(
  attempt: number,
  baseMs = 100,
  maxMs = 2_000,
): number {
  const exp = Math.min(maxMs, baseMs * 2 ** attempt);
  const jitter = 0.5 + Math.random(); // [0.5, 1.5)
  return Math.round(exp * jitter);
}
```

## Testing / Verification

- Timeouts: request returns a stable timeout error within the budget.
- Retries: attempts are bounded; retryable vs non-retryable errors are classified correctly.
- Idempotency: duplicate request/message does not double-apply side effects.
- Bulkheads: dependency overload doesn’t starve unrelated work.
- Breaker: opens under repeated failures and closes after recovery.

## References

- Deeper checklists: `references/checklists.md`
- Instrumentation guidance: `apply-observability-patterns`
- Typed error semantics and explicit lifetimes: `typescript-style-guide`
- Wrapping clients: `apply-structural-patterns` (Proxy/Decorator)

## Output Template

When applying this skill, return:

- The failure model assumptions (retryable errors, idempotency strategy, time budget).
- The minimal code changes (timeouts, retry loop, breaker/bulkhead wrapper).
- The verification steps (tests + how to simulate failure locally).
