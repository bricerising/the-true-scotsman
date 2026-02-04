# Self-contained service

## Intent
Build a vertical slice service that owns UI/API/data logic for a user-facing feature to reduce cross-service coordination.

## Use when
- You want fast end-to-end iteration for a feature without coordinating changes across many services.
- The slice can reasonably own its data and present a coherent UI/API surface.

## Avoid / watch-outs
- Avoid duplicating shared domain logic inconsistently; prefer clear ownership and explicit contracts.
- Ensure cross-cutting standards (auth/telemetry/resilience) remain consistent across slices.

## Skill mapping
- `architecture`: choose slice boundaries and integration points.
- `platform`: provide a shared “chassis” so each slice has consistent boundary behavior.
- `spec`: define end-user flows + contract expectations.
