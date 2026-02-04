# Decompose by business capability

## Intent
Define service boundaries around business capabilities (e.g., “Billing”, “Catalog”), not technical layers.

## Use when
- You want services that can evolve independently with clear ownership and APIs.
- You can align code, data, and operational responsibility to the same capability boundary.

## Avoid / watch-outs
- Don’t slice into “UI service / service layer / DB service”; that recreates layered coupling over the network.
- Capabilities should own their data (prefer Database per service) to avoid shared-schema coupling.

## Skill mapping
- `architecture`: propose candidate capabilities + integration seams.
- `spec`: define capability APIs/events and non-goals.
- `platform`: standardize cross-cutting concerns once multiple capabilities exist.
