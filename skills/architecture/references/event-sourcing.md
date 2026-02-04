# Event sourcing

## Intent
Persist state changes as an append-only sequence of events and reconstruct current state by replaying them.

## Use when
- You need strong auditability/temporal correctness and the ability to rebuild projections.
- The domain benefits from explicit event histories (debugging, analytics, replay).

## Avoid / watch-outs
- Event sourcing is not a free upgrade; it adds projection rebuild, schema evolution, and ops complexity.
- Plan event versioning and migration strategies early.

## Skill mapping
- `spec`: event schemas, versioning, replay rules, and rebuild acceptance criteria.
- `observability`: replay/projection metrics and debuggability.
- `testing`: tests for event replay/projection correctness and backward compatibility.
