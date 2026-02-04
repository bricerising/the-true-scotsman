# Service mesh

## Intent
Use infrastructure proxies to provide service-to-service networking features (mTLS, routing, retries, telemetry) consistently.

## Use when
- You need consistent networking/security controls across many services and languages.
- You want standardized telemetry and traffic management (canaries, routing rules).

## Avoid / watch-outs
- A mesh doesn’t remove the need to design correct app semantics (idempotency, time budgets, error mapping).
- Operational complexity is high; ensure you can operate and debug the mesh itself.

## Skill mapping
- `architecture`: decide what belongs in mesh vs app and document failure semantics.
- `observability`: correlate app telemetry with proxy/mesh telemetry.
- `resilience`: ensure retries/timeouts align across layers to avoid retry storms.
