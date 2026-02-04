# API Gateway / Backends for Frontends (BFF)

## Intent
Provide a single entry point (or one per client) that routes/aggregates requests to internal services and applies cross-cutting concerns.

## Use when
- External clients would otherwise call many internal services (chatty, brittle).
- You need protocol translation, centralized auth, or consistent rate limiting at the edge.
- Different clients need different APIs without forcing internal services to support all shapes (BFF).

## Avoid / watch-outs
- Avoid turning the gateway into a “smart monolith” by putting domain logic there.
- Watch fan-out latency and N+1 calls; set time budgets and concurrency limits.
- Make error mapping/versioning explicit; the gateway amplifies contract drift.

## Skill mapping
- `spec`: define public API shape, error semantics, and deprecation/versioning.
- `security`: authn/authz at the edge; careful logging/PII discipline.
- `resilience`: timeouts, retries policy, and bulkheads for fan-out to downstream services.
- `observability`: per-route RED metrics + trace/log correlation across downstream calls.
- `platform`: shared gateway middleware/wrappers when multiple gateways or BFFs exist.
- `testing`: consumer-visible tests for response shapes and failure behavior.
