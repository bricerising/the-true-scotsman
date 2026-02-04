# Anti-corruption layer

## Intent
Protect your domain model by translating/isolating external or legacy models at the boundary.

## Use when
- Integrating with a legacy system or third-party API that has different concepts and semantics.
- Migrating a monolith or crossing bounded-context boundaries.

## Avoid / watch-outs
- Keep the boundary thin: translate and validate, don’t accumulate business logic in the adapter.
- Make mapping failures explicit (typed errors); log safely and keep PII out of telemetry.

## Skill mapping
- `architecture`: define context boundaries and integration approach.
- `design`: implement the translation layer (Adapter/Facade) with clear ownership.
- `security`: validate inputs and protect secrets/PII at the boundary.
- `observability`: instrument translation failures with correlation IDs.
