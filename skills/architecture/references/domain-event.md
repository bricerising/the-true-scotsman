# Domain event

## Intent
Represent a business fact as an event so other parts of the system can react without tight coupling.

## Use when
- Side effects and integrations should be decoupled from the core transaction (async reactions).
- You need a stable “contract” for other services to build on (replication, notifications, analytics).

## Avoid / watch-outs
- Avoid leaking internal schemas; define versioned event contracts with stable semantics.
- Events are at-least-once in practice; consumers must handle duplicates safely.

## Skill mapping
- `spec`: event schema, versioning rules, and ordering/duplication expectations.
- `resilience`: idempotent consumers and retry/backoff with DLQ strategy.
- `observability`: correlation IDs across publish/consume; lag and failure metrics.
