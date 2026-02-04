# Sidecar

## Intent
Run a helper process alongside a service instance to provide cross-cutting functionality (proxy, agent, config, telemetry).

## Use when
- You want to offload concerns from the app process without requiring app-language integrations.
- You need per-instance helpers (proxies, log/metric agents) managed with the service lifecycle.

## Avoid / watch-outs
- Sidecars add moving parts; define ownership, upgrades, and observability for the sidecar itself.
- Ensure app/sidecar lifecycle coordination is robust (startup order, readiness semantics).

## Skill mapping
- `platform`: standardize sidecar configs and lifecycle wiring.
- `observability`: telemetry for sidecar health and its impact on app behavior.
- `resilience`: clarify failure behavior when the sidecar is unhealthy.
