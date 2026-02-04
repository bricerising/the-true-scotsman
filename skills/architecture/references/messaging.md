# Messaging

## Intent
Integrate services asynchronously using messages/events via a broker (queues/topics/streams).

## Use when
- You want temporal decoupling: producers don’t need consumers to be up to accept work.
- The workflow tolerates eventual consistency and at-least-once delivery semantics.

## Avoid / watch-outs
- Messages can be duplicated/reordered; consumers must be idempotent and resilient.
- Define schemas/contracts; uncontrolled event evolution causes brittle consumers.

## Skill mapping
- `architecture`: pick eventing vs RPC, and define ownership and ordering expectations.
- `resilience`: idempotent consumer, dedupe/inbox, retry/backoff, DLQ strategy.
- `spec`: message schemas, versioning rules, and failure semantics.
- `observability`: lag metrics, correlation IDs, and message-type attributes on spans/logs.
- `testing`: consumer-visible tests for duplicate/retry and poison-message behavior.
