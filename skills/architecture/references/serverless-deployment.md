# Serverless deployment

## Intent
Deploy services as managed functions where the platform handles scaling and runtime management.

## Use when
- Workloads are bursty and fit within execution limits; you want reduced operational burden.
- You can tolerate platform constraints (cold starts, limited runtime control).

## Avoid / watch-outs
- Cold starts and concurrency limits can impact latency; be explicit about SLOs.
- Observability and local debugging can be harder; invest in tracing/logging.

## Skill mapping
- `spec`: define latency and availability requirements under cold starts/bursts.
- `observability`: ensure traces/logs/metrics work in the serverless environment.
- `resilience`: time budgets and retry strategy aligned to function execution limits.
