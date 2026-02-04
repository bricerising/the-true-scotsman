# API Composition

## Intent
Implement a query by calling multiple services and composing the results (often via a dedicated “API composition” component).

## Use when
- A client needs data owned by multiple services, and you can’t (or won’t) denormalize into a read model.
- You need a single “view” API that hides internal service boundaries from clients.

## Avoid / watch-outs
- Composition can become slow and failure-prone under fan-out; apply strict time budgets and concurrency limits.
- Beware N+1 call graphs; prefetch in batches or change the API shape.
- If composition becomes a hotspot, consider CQRS/read models instead.

## Skill mapping
- `architecture`: decide composition vs CQRS vs duplication/replication.
- `resilience`: per-dependency timeouts/bulkheads; partial failure strategy.
- `observability`: trace fan-out and record which dependencies contributed to latency/errors.
- `spec`: define response semantics under partial failure (best-effort vs fail-fast).
- `testing`: tests for response semantics and degraded-mode behavior.
