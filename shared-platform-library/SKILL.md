---
name: shared-platform-library
description: Design and maintain a shared platform library (e.g. `packages/shared`) that standardizes cross-cutting concerns across services (auth, config, gRPC/HTTP helpers, lifecycle, typed errors/results, observability, retries/timeouts). Use when multiple services duplicate boundary logic or when introducing shared primitives without creating a “utils junk drawer”.
---

# Shared Platform Library

## Overview

Create a small, disciplined “shared kernel” that drives cohesion across services by providing stable primitives at boundaries (auth, RPC, config, telemetry, resilience, lifecycles).

The goal is not reuse-for-reuse’s-sake; it’s consistent behavior and lower cognitive load across a system.

## Workflow

1. Define the “platform surface” (what belongs here vs per-service).
2. Inventory repetition across services and pick 1–2 extractions with the highest leverage.
3. Design the module boundaries and dependency direction (avoid cycles, keep exports stable).
4. Design APIs that are:
   - explicit about inputs/outputs and expected failures (`Result` / tagged errors)
   - explicit about lifetimes (create/start/stop/dispose)
   - explicit about cancellation/time budgets (`AbortSignal`, deadlines)
   - explicit about telemetry fields (trace/log/metrics correlation)
5. Implement minimal primitives + one “golden path” usage in at least two services.
6. Add tests at the seam (unit tests for primitives + characterization tests for adopters if needed).
7. Document usage and deprecation/migration guidance.

## What Belongs In The Shared Platform Library

Prefer **boundary primitives** over “random helpers”:

- Auth/JWT verification utilities
- gRPC server/client helpers (handler wrappers, interceptors, service registration)
- HTTP client wrappers (timeouts, retries, tracing hooks)
- Typed error/result primitives and decoding helpers
- Lifecycle helpers (start/stop guards, “agent” patterns, shutdown coordination)
- Observability glue (log field mixins, span helpers, RED metric helpers)
- Resilience glue (retry helpers, circuit breaker/bulkhead primitives where applicable)

## What Does *Not* Belong

- Business/domain logic (poker rules, billing rules, table invariants, etc.)
- One-off utilities used by one call site (“utils junk drawer” risk)
- Hidden I/O at import time (no global clients created on module load)
- High-cardinality or PII-heavy telemetry helpers (keep privacy discipline explicit)

## Guardrails (Opinionated Defaults)

- “Two consumers” rule: don’t add a primitive until it’s used (or imminently needed) in 2+ services.
- Keep the public surface small: a few stable entrypoints beat dozens of micro-exports.
- Prefer composition over inheritance; “wrappers” should preserve response shapes and error semantics.
- Make operation names explicit (don’t depend on framework reflection/casing quirks).
- Keep dependencies minimal; avoid pulling in large frameworks into every service accidentally.
- If you introduce retries, you must introduce idempotency guidance.

## Pattern Catalogue (Common Shared Primitives)

- **Boundary handler wrappers (Template Method + interceptors)**: standardize “decode → call → map response” with consistent timing/logging/error mapping.
- **Client proxies**: wrap callback APIs into promises with `AbortSignal` support and timeouts.
- **Lifecycle facades**: stable `start()/stop()` APIs with concurrency guards to avoid start/stop races.
- **Service registration validators**: fail fast if a server registers an incomplete handler set.

## References

- Checklists: `references/checklists.md`
- Module layout guidance: `references/module-layout.md`
- Templates/snippets: `references/templates.md`
- Boundary wrappers (error/idempotency/telemetry contracts): `references/boundary-wrappers.md`

Related skills:

- `spec-driven-development` (spec bundles + contracts)
- `apply-observability-patterns` (telemetry expectations)
- `apply-resilience-patterns` (timeouts/retries/idempotency)
- `typescript-style-guide` (typed boundaries/errors/lifetimes)
- `apply-structural-patterns` / `apply-behavioral-patterns` (wrappers/pipelines)

## Output Template

When applying this skill, return:

- Proposed module(s) and public API surface (what’s exported).
- What duplication this removes (call sites) and what invariants it enforces.
- Error semantics, cancellation/timeouts strategy, and telemetry fields.
- Adoption plan (first two migrations) + tests/verification.
