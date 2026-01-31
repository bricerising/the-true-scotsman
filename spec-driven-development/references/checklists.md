# Spec Quality Checklist (AI-Friendly)

Use this to review a spec before implementation (or when a spec has drifted).

## Scope & Intent

- The problem statement is 1–3 paragraphs and names the affected services/boundaries.
- Goals and non-goals are explicit (prevents scope creep).
- Definitions exist for ambiguous terms (domain vocabulary, “table”, “session”, “order”, etc.).

## Acceptance & Testability

- Each user story has an “independent test” statement.
- Acceptance criteria are written in observable terms (Given/When/Then or equivalent).
- Edge cases are listed (at least: invalid input, permission/auth, timeouts/downstream errors).

## Contracts

- External contracts are documented (OpenAPI/proto/message schemas).
- Error semantics are explicit and stable (error codes/variants, not free-form strings).
- Versioning expectations are written down (additive vs breaking changes).

## Ownership & Consistency

- Data ownership/source-of-truth is stated for key entities.
- Consistency boundary is clear:
  - what must be strongly consistent
  - what can be eventually consistent
- Idempotency expectations exist for write operations and message consumers.

## Non-Functional Requirements

- Latency budgets and timeouts are stated for key boundaries.
- Concurrency/throughput expectations exist where relevant.
- Privacy/PII constraints are documented.

## Observability & Operations

- Required log fields are stated (including correlation IDs).
- Tracing boundaries and propagation expectations are stated.
- Metrics expectations exist (RED + a few domain metrics).
- There is a minimal “how to verify” section (commands, URLs, smoke checks).

## Change Control

- The spec names the “stop condition” for work (what “done” means).
- If the spec is for a migration/refactor, it includes an incremental plan and rollback considerations.
