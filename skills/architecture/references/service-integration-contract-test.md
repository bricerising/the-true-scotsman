# Service Integration Contract Test

## Intent
Verify that a service integrates correctly with its external dependencies and/or satisfies published contracts in an integration-like environment.

## Use when
- Unit tests are insufficient to validate wiring, serialization, or contract compatibility.
- You want confidence that changes won’t break key consumer/provider expectations.

## Avoid / watch-outs
- Keep these tests focused and deterministic; avoid flaky full-environment tests.
- Define clear test data and cleanup strategies to prevent state leakage.

## Skill mapping
- `testing`: create integration-contract tests at service boundaries (HTTP/gRPC/events).
- `spec`: use contracts and acceptance scenarios as test sources.
- `observability`: ensure failures are diagnosable (logs/trace IDs in test output where possible).
