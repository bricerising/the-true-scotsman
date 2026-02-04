# Service Template

## Intent
Bootstrap new services quickly and consistently using a standard template (repo skeleton + conventions).

## Use when
- You are creating services repeatedly and want consistent defaults (build/deploy, telemetry, lint, tests).
- You want to reduce “setup thrash” and make new services production-ready faster.

## Avoid / watch-outs
- Keep the template lean; a large template becomes hard to update and discourages adoption.
- Ensure upgrades are straightforward (e.g., template updates can be applied incrementally).

## Skill mapping
- `platform`: define the template + keep it aligned with the chassis/shared primitives.
- `spec`: include a minimal spec bundle and quickstart expectations.
- `observability` / `resilience` / `security`: bake in defaults so services start safe by default.
