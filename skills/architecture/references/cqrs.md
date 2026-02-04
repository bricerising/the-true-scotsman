# Command Query Responsibility Segregation (CQRS)

## Intent
Separate the write model (commands) from the read model (queries) so each can evolve and scale independently.

## Use when
- Read and write workloads differ significantly (shape, scale, latency).
- You need denormalized read models or multiple projections optimized for different queries.

## Avoid / watch-outs
- CQRS adds complexity; avoid for simple CRUD when a single model works.
- Be explicit about consistency (staleness) and user-visible semantics.

## Skill mapping
- `architecture`: decide if CQRS is warranted and define projection ownership.
- `spec`: acceptance criteria for eventual consistency and read-your-writes expectations.
- `observability`: projection lag and rebuild visibility.
- `testing`: tests that pin behavior under staleness and rebuild scenarios.
