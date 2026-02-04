# Aggregate

## Intent
Define a consistency boundary (DDD aggregate) that enforces invariants for a cluster of domain objects.

## Use when
- You need to enforce invariants/transactions within a clear boundary.
- You want to prevent “distributed invariants” that would require cross-service transactions.

## Avoid / watch-outs
- Keep aggregates small; large aggregates reduce concurrency and create performance bottlenecks.
- Don’t let “read model needs” expand your aggregate; use CQRS/read models instead.

## Skill mapping
- `architecture`: define service and data ownership boundaries aligned to aggregates.
- `spec`: document invariants and expected failures when invariants are violated.
- `design`: model aggregates with explicit command handling and typed errors.
