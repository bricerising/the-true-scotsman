# Distributed tracing

## Intent
Trace requests end-to-end across service boundaries using correlation IDs and spans.

## Use when
- Always for microservices: you need to debug latency and failures across call graphs.
- You need to attribute work to downstream dependencies and isolate bottlenecks.

## Avoid / watch-outs
- Don’t attach high-cardinality data (raw payloads, unbounded IDs) as span attributes.
- Sampling must preserve error traces; otherwise you lose the most important data.

## Skill mapping
- `observability`: instrument root spans and downstream spans; define stable span names/attributes.
- `resilience`: correlate retries/breakers with trace attributes for debugging.
