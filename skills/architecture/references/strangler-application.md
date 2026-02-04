# Strangler application

## Intent
Incrementally modernize a monolith by routing selected functionality to new services, without a “flag day” rewrite.

## Use when
- You need to migrate safely while preserving existing behavior and availability.
- You can route traffic by path/feature/tenant and progressively expand the new surface.

## Avoid / watch-outs
- Require robust observability and rollback strategies; migrations fail in partial, messy ways.
- Keep a clear deprecation plan and contract compatibility rules.

## Skill mapping
- `spec`: pin existing behavior and compatibility guarantees.
- `architecture`: design routing, cutover phases, and integration seams.
- `observability`: measure correctness (errors/latency) during migration and detect regressions.
- `testing`: add characterization/consumer-visible tests before major refactors.
