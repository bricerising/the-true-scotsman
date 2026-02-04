# Externalized configuration

## Intent
Keep environment-specific configuration outside the deployable artifact so it can vary per environment and be changed safely.

## Use when
- You deploy the same artifact to multiple environments (dev/staging/prod) with different endpoints/secrets.
- You need to rotate secrets, change feature flags, or tune limits without rebuilding images.

## Avoid / watch-outs
- Treat config as part of the contract: validate at startup and fail fast with clear errors.
- Don’t leak secrets in logs/telemetry; apply strict redaction discipline.

## Skill mapping
- `platform`: config loading/validation primitives with explicit schemas.
- `security`: secret handling, redaction, and least privilege for config access.
- `observability`: log effective config version/hash (not secret values) for debugging.
