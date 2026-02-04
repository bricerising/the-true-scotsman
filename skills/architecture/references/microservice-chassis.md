# Microservice chassis

## Intent
Provide a reusable set of cross-cutting capabilities (config, logging, health, telemetry, auth, etc.) that every service uses.

## Use when
- You have (or expect) multiple services that would otherwise re-implement the same boundary behaviors.
- You want consistent operational behavior (telemetry fields, timeouts, error mapping) across services.

## Avoid / watch-outs
- Keep the chassis surface small and stable; avoid turning it into a “utils junk drawer”.
- Prevent tight coupling via deep inheritance; prefer composition and explicit lifetimes.

## Skill mapping
- `platform`: design the shared library surface and adoption plan (2+ services rule).
- `observability`: standardize trace/log/metrics correlation and field contracts.
- `resilience`: enforce timeouts/retries/idempotency as defaults.
- `security`: standardize authn/authz and safe logging/redaction.
