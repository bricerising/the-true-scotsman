# Single Service Instance per Host

## Intent
Run a single service instance on each host to maximize isolation and minimize noisy-neighbor issues.

## Use when
- Isolation and predictable performance matter more than utilization.
- You want simpler capacity and failure-domain reasoning per service.

## Avoid / watch-outs
- Lower density can increase cost; ensure the isolation benefit is worth it.
- Hosts still need consistent provisioning and telemetry.

## Skill mapping
- `architecture`: define deployment isolation requirements and constraints.
- `observability`: host/service metrics and deploy markers for correlation.
