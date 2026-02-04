# Transaction log tailing

## Intent
Publish events by tailing a database’s transaction log (CDC) instead of writing outbox records in application code.

## Use when
- You want to publish change events with minimal app changes, or you need broad coverage of DB changes.
- Your DB/infra supports CDC reliably and you can operate it as platform infrastructure.

## Avoid / watch-outs
- CDC pipelines are operationally complex; validate ordering/duplication semantics carefully.
- Mapping DB changes to domain events can be tricky; avoid leaking internal schemas.

## Skill mapping
- `architecture`: choose CDC vs outbox; define event semantics and ownership.
- `platform`: operate CDC pipeline and standardize event envelopes.
- `spec`: contract for emitted events and schema evolution.
- `observability`: lag/throughput metrics and failure alerting for the CDC pipeline.
