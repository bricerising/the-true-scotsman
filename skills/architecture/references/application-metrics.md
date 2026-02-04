# Application metrics

## Intent
Expose metrics that make service health and performance measurable (request volume, errors, latency, and domain signals).

## Use when
- Always: metrics are a prerequisite for operating distributed systems reliably.
- You need alerting, capacity planning, and debugging signals beyond logs.

## Avoid / watch-outs
- Avoid high-cardinality labels (user IDs, raw URLs, unbounded IDs).
- Metrics should be stable contracts; changing names/labels breaks dashboards/alerts.

## Skill mapping
- `observability`: define the field/label contract and implement RED + domain metrics.
- `spec`: document SLOs and how metrics reflect success/failure semantics.
