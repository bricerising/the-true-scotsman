# Circuit Breaker

## Intent
Prevent cascading failures by failing fast when a dependency is unhealthy instead of repeatedly sending requests that are likely to fail or time out.

## Use when
- A downstream dependency becomes flaky/unavailable and causes retries/timeouts to pile up.
- You want to protect your own resources (threads, pools, event loop) under partial failure.

## Avoid / watch-outs
- Breakers need a recovery/probing strategy (half-open) and a UX/fallback plan.
- Avoid hiding persistent errors; surface stable error codes and make behavior observable.

## Skill mapping
- `resilience`: configure breaker thresholds, time budgets, and fallbacks; expose breaker metrics.
- `observability`: log breaker state transitions and correlate with dependency errors/latency.
- `testing`: simulate dependency failure and assert breaker open/close behavior where appropriate.
