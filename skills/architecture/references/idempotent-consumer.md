# Idempotent Consumer

## Intent
Make message consumption safe under at-least-once delivery by tolerating duplicates and replays.

## Use when
- You consume messages/events from a broker where duplicates are possible (most systems).
- You retry on failures and need to guarantee side effects aren’t applied twice.

## Avoid / watch-outs
- Dedupe requires a stable idempotency key and a persistence strategy (inbox/dedupe table).
- Beware unbounded dedupe storage; define TTL and reconciliation strategy.

## Skill mapping
- `resilience`: dedupe/inbox patterns, retry/backoff, and poison message handling.
- `spec`: define idempotency keys and duplicate delivery expectations.
- `testing`: tests that prove duplicates don’t double-apply side effects.
