# Microservice Architecture

## Intent
Build an application as a suite of small, independently deployable services that collaborate over the network.

## Use when
- You need independent deployability, scaling, and release cadence across parts of the system.
- Teams need clearer ownership boundaries and autonomy (and you can invest in DevEx/ops).
- The domain naturally decomposes into capabilities/subdomains with stable contracts.

## Avoid / watch-outs
- Don’t decompose “just because”; microservices add latency, operational overhead, and harder debugging.
- Avoid tight coupling via shared databases or synchronous call graphs that recreate a distributed monolith.
- Require strong fundamentals: `spec`/contracts, `observability`, and `resilience` guardrails.

## Skill mapping
- `architecture`: pick decomposition + integration style; avoid “pattern soup”.
- `spec`: define contracts, versioning rules, and failure semantics.
- `observability`: log/trace/metrics correlation across boundaries.
- `resilience`: timeouts, idempotency, retries, and bulkheads to survive partial failure.
- `platform`: shared primitives (auth/config/telemetry wrappers) when 2+ services repeat them.
