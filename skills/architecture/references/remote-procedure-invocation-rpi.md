# Remote Procedure Invocation (RPI)

## Intent
Integrate services using synchronous request/response calls (HTTP/gRPC) as if invoking a remote procedure.

## Use when
- The caller needs an immediate answer to proceed (tight request/response workflow).
- The coupling is acceptable and contracts are stable, versioned, and tested.

## Avoid / watch-outs
- Synchronous chains amplify tail latency and cascade failures; keep call graphs shallow.
- Retries require idempotency; set explicit timeouts and cancellation budgets.

## Skill mapping
- `resilience`: timeouts + bounded retries; circuit breakers for flaky dependencies.
- `spec`: explicit error semantics, SLAs, and compatibility/versioning.
- `observability`: traces spanning the full synchronous chain with stable `op` naming.
