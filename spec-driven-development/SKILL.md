---
name: spec-driven-development
description: Write and maintain specification-first artifacts for enterprise web applications (service specs, API contracts, plans, task lists, and quickstarts). Use when starting a new feature/service, refactoring major behavior, defining non-functional requirements, or when agents need a shared source of truth for scope, acceptance criteria, and invariants.
---

# Spec Driven Development

## Overview

Create a stable “source of truth” for agents and humans: write specs with testable acceptance criteria and keep them aligned with implementation.

This skill treats specs as **operational tooling**: they prevent scope drift, enforce invariants, and make AI iteration converge.

## Core Idea

- Specs define **what must be true** (contracts, scenarios, invariants, NFRs), not “how we coded it”.
- Plans/tasks define **how we’ll get there** (phases, work breakdown, acceptance per task).
- Code + tests are the proof.

## Where Specs Live (Opinionated)

Use one (or both) of these:

- **System specs**: `specs/*.md` for cross-service rules and shared constraints (auth, observability, eventing, product scope).
- **Service spec bundle**: `apps/<service>/spec/` for service-local truth:
  - `spec.md`: requirements and acceptance scenarios
  - `contracts/`: OpenAPI/proto/WS message contracts
  - `data-model.md`: domain entities + storage boundaries
  - `plan.md`: phases and wiring/structure
  - `tasks.md`: checklist-style backlog with acceptance criteria
  - `quickstart.md`: how to run/verify the service in dev

## Workflow

1. Decide the scope:
   - One service? write/update the service spec bundle.
   - Cross-service or product-wide? write/update a system spec.
2. Write acceptance-first:
   - user story + “independent test”
   - acceptance scenarios (Given/When/Then)
   - edge cases and invariants (“constitution requirements”)
3. Lock down contracts:
   - HTTP/gRPC schemas, message types, error codes, idempotency keys
   - versioning rules and backward compatibility expectations
4. Add non-functional requirements (NFRs) that matter:
   - latency budgets, concurrency, durability, audit, privacy
   - observability and resilience requirements (trace/log/metrics, timeouts/retries/idempotency)
5. Break it into tasks with acceptance:
   - keep tasks small and orderable
   - each task has an observable acceptance check
6. Implement and keep docs honest:
   - if implementation forces a change in behavior, update specs first
   - keep quickstarts and contracts current

## Guardrails

- “No spec, no change”: don’t implement major behavior without updating the spec surface.
- Don’t hide requirements in code; put them in `spec.md` where agents can find them.
- Keep contracts stable; prefer additive changes and version explicitly when you can’t.
- Write down **non-goals** to stop scope creep.

## References

- Templates: `references/templates.md`
- Spec quality checklist: `references/checklists.md`
- Architecture choices: `select-architecture-pattern`
- In-process pattern choices: `select-design-pattern`
- Typed boundaries/errors/lifetimes: `typescript-style-guide`
- Consumer-visible tests: `consumer-test-coverage`
