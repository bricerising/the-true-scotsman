---
name: consumer-test-coverage
description: Create or expand consumer-centric test suites and coverage for microservices (gRPC/HTTP handlers, service flows, event consumers, caches, jobs, observability) while preserving behavior. Use when asked to add tests, raise coverage, or validate consumer-facing behavior across services.
---

# Consumer Test Coverage

## Overview

Improve coverage by exercising consumer-visible behavior with infra mocked and behavior preserved.

## Workflow

1. Identify consumer-facing flows: handlers, service APIs, event consumers, caches, jobs.
2. Map expectations from specs or existing tests.
3. Add tests for both success and error paths.
4. Mock infra boundaries (DB, Redis, network, schedulers).
5. Run coverage and iterate until thresholds are met.

## Testing Patterns

- Handler paths: call handler with mocked service, assert response, metrics, and error handling.
- Event consumers: feed mixed payload shapes (missing type, struct/list values, invalid entries).
- Cache/storage: cover cache hit/miss, null/empty results, invalidation behavior.
- Jobs: use fake timers; cover interval runs and error logging branches.
- Observability: assert metrics render and logging mixins without external services.

## Guardrails

- Preserve externally visible behavior and API shapes.
- Avoid real network/listen calls in unit tests; mock them.
- Keep tests consumer-focused; do not assert internal implementation details beyond outputs/side effects.

## Commands

- `cd apps/<service> && npm test -- --coverage`
