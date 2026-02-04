# Server-side page fragment composition

## Intent
Compose a page on the server from fragments produced by multiple services (micro-frontends rendered server-side).

## Use when
- You need server-side rendering (SEO, first-load performance) while retaining team autonomy for UI slices.
- You want to hide internal services from browsers and centralize auth/caching.

## Avoid / watch-outs
- Fragment composition can become a fan-out hotspot; apply time budgets, caching, and fallbacks.
- Define consistent error handling so one fragment doesn’t break the entire page.

## Skill mapping
- `architecture`: decide composition boundaries and caching strategy.
- `resilience`: concurrency limits/bulkheads; partial failure semantics.
- `observability`: trace fan-out and log which fragments contributed to latency/errors.
- `spec`: page contract (what is required vs optional) and degraded-mode rules.
