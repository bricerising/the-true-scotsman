# Shared database

## Intent
Multiple services access the same database/schema directly.

## Use when
- Transitional state during migration, or when organizational/operational constraints require it temporarily.

## Avoid / watch-outs
- Shared schemas create tight coupling and make independent deployment/versioning difficult.
- Schema changes become cross-team coordination events; failure domains widen.

## Skill mapping
- `architecture`: treat as a migration phase; define an exit strategy toward owned schemas (Database per service).
- `spec`: make coupling explicit and document compatibility rules for schema changes.
- `testing`: add characterization tests to catch accidental breaking schema changes.
