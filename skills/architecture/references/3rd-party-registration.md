# 3rd Party Registration

## Intent
Use an external system (orchestrator/infra component) to register/deregister service instances in the registry.

## Use when
- Your infrastructure can observe instance lifecycle better than the app (e.g., orchestrator events).
- You want to avoid shipping registry credentials and registration logic in every service.

## Avoid / watch-outs
- Ensure registration reacts quickly to crashes and deployments; stale registry data breaks routing.
- Clarify ownership: who operates the registrar and how it’s monitored.

## Skill mapping
- `architecture`: define responsibilities between app and platform/orchestrator.
- `platform`: standardize service metadata needed for registration (name, version, env, health endpoints).
- `observability`: monitor registrar health, churn, and stale instance counts.
