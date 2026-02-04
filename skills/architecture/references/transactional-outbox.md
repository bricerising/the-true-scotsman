# Transactional outbox

## Intent
Avoid dual-write bugs by writing domain state + an outbox record in the same DB transaction, then publishing asynchronously.

## Use when
- You need reliable event publication tied to a database transaction.
- You integrate via async events and can accept at-least-once delivery.

## Avoid / watch-outs
- Requires idempotent consumers; duplicates will happen.
- Needs monitoring for outbox backlog and publisher failures.

## Skill mapping
- `architecture`: choose outbox vs CDC (transaction log tailing) and define event ownership.
- `resilience`: publisher retry/backoff; consumer idempotency/dedupe.
- `observability`: lag metrics and correlation across publish/consume.
- `spec`: event schemas, ordering/duplication expectations, and compatibility.
- `platform`: shared outbox publisher when 2+ services need it.
