# Saga

## Intent
Implement a cross-service business transaction as a sequence of local transactions coordinated with messages, including compensating actions on failure.

## Use when
- A workflow spans multiple services and must handle partial failure without distributed transactions.
- You can model compensations (undo) or alternative paths explicitly.

## Avoid / watch-outs
- Don’t use sagas to “fake” strong consistency; model the business reality and compensations.
- Make the saga state machine explicit and observable; implicit workflow is un-debuggable.

## Skill mapping
- `architecture`: pick orchestration vs choreography; define the workflow states.
- `resilience`: idempotency, retries/backoff, and DLQ strategy for each step.
- `observability`: correlation IDs across steps; metrics for state transitions and time spent.
- `testing`: tests for happy path + compensations + duplicate delivery.
