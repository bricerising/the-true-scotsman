# Server-side service discovery

## Intent
Clients call a router/load balancer, which queries the service registry and forwards requests to instances.

## Use when
- You want “dumb clients” and centralized control over routing, balancing, and rollout behavior.
- You need consistent behavior across many client types (web, mobile, scripts, partner integrations).

## Avoid / watch-outs
- Routers can become a scaling and reliability bottleneck; design for HA and capacity.
- Avoid pushing business logic into routing layers (keep it as infrastructure concerns).

## Skill mapping
- `architecture`: define routing boundaries and what cross-cutting concerns belong there.
- `platform`: standardize routing middleware, auth hooks, and telemetry enrichment.
- `observability`: per-route metrics and traces that propagate across forwarded hops.
