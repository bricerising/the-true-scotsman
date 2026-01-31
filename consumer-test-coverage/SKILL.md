---
name: consumer-test-coverage
description: Create or expand consumer-centric test suites and coverage for microservices (gRPC/HTTP handlers, service flows, event consumers, caches, jobs, observability) while preserving behavior. Use when asked to add tests, raise coverage, or validate consumer-facing behavior across services.
---

# Consumer Test Coverage

## Overview

Improve coverage by exercising consumer-visible behavior with infra mocked and behavior preserved.

## Workflow

1. Read relevant specs (system + service) and map them to consumer-visible flows and invariants.
2. Identify consumer-facing entrypoints: HTTP/gRPC handlers, public service methods, event consumers, cache/storage adapters, jobs.
3. Add tests for success and failure paths that a consumer can observe (invalid input, downstream failures, permissions, timeouts where applicable).
4. Mock infra boundaries (DB, Redis, network listeners, clocks/timers). Prefer calling handlers/functions directly instead of running real servers.
5. Run focused coverage and iterate until the target is met (default 80% unless the spec says otherwise).

## Testing Patterns

- Handler paths: call handler with mocked service, assert response, metrics, and error handling.
- Event consumers: feed mixed payload shapes (missing type, struct/list values, invalid entries).
- Cache/storage: cover cache hit/miss, null/empty results, invalidation behavior.
- Jobs: use fake timers; cover interval runs and error logging branches.
- Observability: assert metrics render and logging mixins without external services.
  - Vitest note: if mocked values are referenced by `vi.mock` factories, use `vi.hoisted` to avoid init-order bugs.

## Guardrails

- Preserve externally visible behavior and API shapes.
- Avoid real network/listen calls in unit tests; mock them.
- Keep tests consumer-focused; do not assert internal implementation details beyond outputs/side effects.

## Commands

- Vitest example: `npx vitest run apps/<service>/**/*.test.ts --coverage --coverage.include='apps/<service>/src/**'`
- Generic: `cd apps/<service> && npm test -- --coverage`
