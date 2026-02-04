# Service deployment platform

## Intent
Provide a platform that standardizes how services are built, deployed, scaled, and operated.

## Use when
- You have many services and want consistent deployment, observability, and security defaults.
- You want to reduce cognitive load and make “the right way” the easy way.

## Avoid / watch-outs
- Platform scope creep is real; keep a clear product surface and versioning.
- Ensure platform changes don’t cause system-wide incidents; treat platform as critical infra.

## Skill mapping
- `platform`: define shared primitives, templates, and upgrade paths.
- `observability`: platform-level telemetry standards and dashboards.
- `security`: baseline hardening and secret distribution practices.
