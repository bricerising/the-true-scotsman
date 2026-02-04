# Client-side service discovery

## Intent
Service clients query the service registry and load-balance requests across instances themselves.

## Use when
- You can ship a discovery client library in each language/runtime that needs it.
- You want clients to make routing decisions (LB strategy, zone awareness) without a centralized router.

## Avoid / watch-outs
- Every client becomes “smart”: configuration drift and multi-language consistency get hard.
- Treat registry and discovery as part of your dependency graph; apply resilience patterns.

## Skill mapping
- `platform`: shared discovery client and request wrappers.
- `resilience`: timeouts/retries/breakers and concurrency limits in clients.
- `observability`: record routing decisions and correlate failures across retries/instances.
