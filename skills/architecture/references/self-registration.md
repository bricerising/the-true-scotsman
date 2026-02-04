# Self Registration

## Intent
Each service instance registers itself with the service registry and deregisters on shutdown.

## Use when
- Instances can reach the registry and you want self-contained startup/shutdown behavior.
- You can safely distribute registry credentials/config to each instance.

## Avoid / watch-outs
- Handle crashes: ensure the registry removes dead instances (TTL/heartbeats).
- Registration logic must be reliable and observable; otherwise you get “ghost” or missing instances.

## Skill mapping
- `platform`: lifecycle helpers for register/deregister and health/heartbeat behavior.
- `observability`: metrics/logs for registration state and failures.
- `resilience`: retries/backoff for registration with strict time budgets.
