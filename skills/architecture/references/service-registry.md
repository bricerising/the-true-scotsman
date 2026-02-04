# Service registry

## Intent
Keep a directory of service instances so clients/routers can discover where to send requests.

## Use when
- Service instances are dynamic (autoscaling, containers, ephemeral IPs) and you can’t hardcode locations.
- You need a single place to coordinate discovery, health, and routing decisions.

## Avoid / watch-outs
- The registry becomes critical infrastructure; plan HA, failure modes, and operational ownership.
- Discovery alone doesn’t solve reliability; clients still need timeouts and sane retry behavior.

## Skill mapping
- `architecture`: choose discovery approach (client-side vs server-side vs mesh).
- `platform`: provide client/router helpers so discovery is consistent across services.
- `resilience`: timeouts + circuit breakers around calls to discovered instances.
- `observability`: metrics/logs for lookup failures, routing decisions, and health state.
