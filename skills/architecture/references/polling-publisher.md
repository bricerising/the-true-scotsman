# Polling publisher

## Intent
Publish events by periodically polling a database table (often an outbox table) and sending new entries to a broker.

## Use when
- You want a simple implementation path for outbox publication.
- Latency requirements are modest and polling cadence is acceptable.

## Avoid / watch-outs
- Polling introduces delay and load; ensure indexing and backpressure controls.
- Treat publication as at-least-once; consumers still need idempotency.

## Skill mapping
- `resilience`: retries/backoff for publisher; idempotent consumer requirements.
- `observability`: outbox lag/backlog and publisher error metrics.
- `platform`: shared publisher implementation when multiple services need it.
