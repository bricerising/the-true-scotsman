# Health Check API

## Intent
Expose endpoints that report service liveness/readiness so orchestrators and operators can manage instances safely.

## Use when
- Always in production services: orchestrators need readiness/liveness to route traffic correctly.
- You want to implement safe deploys and reduce blast radius during partial failures.

## Avoid / watch-outs
- Don’t make health checks depend on every downstream dependency; distinguish “ready” vs “degraded”.
- Rate-limit and keep checks fast; health checks themselves shouldn’t cause load issues.

## Skill mapping
- `observability`: define liveness/readiness semantics and implement consistent endpoints.
- `resilience`: decide how dependency health affects readiness and load shedding.
- `platform`: provide shared health check helpers across services.
