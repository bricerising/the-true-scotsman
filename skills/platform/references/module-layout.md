# Module Layout (Opinionated)

The shared platform library should feel like a small standard library for the repo: stable, boring, and predictable.

## Recommended Top-Level Modules

Group by *cross-cutting concern*, not by “utils”:

- `auth/`: JWT verification, key providers, auth header helpers
- `config/`: env decoding/validation, typed config objects
- `errors/`: typed errors + helpers to normalize `unknown`
- `result/`: `Result<T, E>` utilities and constructors
- `grpc/`: server/client helpers, handler wrappers, interceptors, service registration
- `http/`: client/server helpers (lightweight; avoid frameworks)
- `lifecycle/`: start/stop/dispose patterns; shutdown coordination
- `observability/`: logger mixins (traceId/spanId), metrics primitives, tracing helpers
- `retry/`: backoff helpers, retry policies (paired with idempotency guidance)
- `proxy/`: safe wrappers around clients (timeouts, cancellation, logging)
- `redis/` / `pg/`: lightweight helpers and conventions; avoid hiding business queries here

## Public API Surface

- Keep a stable `src/index.ts` that re-exports the “supported” surface.
- Prefer explicit exports over `export *` when the surface is large.
- Avoid barrel exports that accidentally import heavy dependencies into every consumer.

## Dependency Direction (Avoid Cycles)

Try to keep a leaf-to-root direction like:

- `types/`, `result/`, `errors/` are leaves.
- `config/` and low-level helpers depend only on leaves.
- `observability/` depends on leaves (and maybe `config/`), but shouldn’t depend on `grpc/`.
- `grpc/` and `http/` depend on leaves + `observability/` (for consistent instrumentation).
- `lifecycle/` can be a leaf-ish utility used by server/client constructors.

If you hit a cycle:

- Extract shared *types* to a leaf module.
- Invert the dependency (pass a callback instead of importing).
- Move wiring to a composition root in the consuming service.

## “Two Consumers” Rule

Don’t add a module until:

- it has 2+ real consumers, or
- it is a prerequisite for a planned second consumer in the same PR series.

This prevents the shared library from becoming a dumping ground for one-off code.
