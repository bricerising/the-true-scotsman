# Multiple service instances per host

## Intent
Run multiple service instances on the same host to improve utilization/density.

## Use when
- Cost/utilization pressure matters and you can tolerate some shared-blast-radius risk.
- You have good isolation controls (resource limits, cgroups, QoS, noisy-neighbor protections).

## Avoid / watch-outs
- Noisy-neighbor and shared resource contention are common failure modes.
- Debugging can get harder; ensure per-instance observability and clear resource metrics.

## Skill mapping
- `observability`: host-level + service-level metrics and correlation for contention incidents.
- `resilience`: bulkheads/concurrency limits to avoid self-saturation under contention.
- `platform`: standardize deployment configs/limits so every service doesn’t reinvent them.
