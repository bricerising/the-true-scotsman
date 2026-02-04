# Service Component Test

## Intent
Test a service as a component with real internal wiring while replacing external dependencies with test doubles.

## Use when
- You want confidence in the service’s behavior without running an entire distributed system.
- You want consumer-visible tests that exercise handlers/consumers/jobs in near-real conditions.

## Avoid / watch-outs
- Avoid real network listeners when possible; call handlers directly and mock adapters.
- Keep dependency doubles realistic (response shapes, timeouts, error codes).

## Skill mapping
- `testing`: add component tests for handlers/consumers/jobs with mocked infra.
- `resilience`: simulate downstream failures to validate timeouts/retries/idempotency behavior.
- `observability`: optionally verify log/trace correlation fields locally.
