# Service instance per container

## Intent
Package each service instance as a container for consistent build/run/deploy behavior.

## Use when
- You want predictable environments and standardized deployment tooling.
- You use an orchestrator (Kubernetes, ECS, Nomad) that manages scheduling and health.

## Avoid / watch-outs
- Containers are not full isolation; still define resource limits and security boundaries.
- Ensure image supply-chain hygiene and consistent base images/tooling.

## Skill mapping
- `platform`: service template/chassis that bakes in health/telemetry defaults.
- `security`: image/dependency hygiene and secrets handling.
- `observability`: standard labels/fields for container metadata and version markers.
