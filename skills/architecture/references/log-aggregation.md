# Log aggregation

## Intent
Centralize structured logs from all services so they can be searched and correlated during debugging and incident response.

## Use when
- Always in distributed systems: local logs are not sufficient for cross-service debugging.
- You need to correlate failures with deployments, traces, and metrics.

## Avoid / watch-outs
- Enforce structured logging and stable fields (service/env/op/traceId).
- Avoid logging secrets/PII; define and enforce redaction policies.

## Skill mapping
- `observability`: structured log field contract and trace correlation.
- `security`: safe logging/redaction and retention policy alignment.
