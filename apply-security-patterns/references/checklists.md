# Security Checklist (Deeper)

Use this as a pressure-driven checklist; apply the relevant items to the boundary you’re changing.

## Authn

- Validate tokens (issuer/audience/expiry); reject `alg=none`; validate signature with correct key.
- If using sessions/cookies: set `HttpOnly`, `Secure`, `SameSite` appropriately; protect state-changing routes with CSRF.

## Authz

- Enforce authorization in the server on every request/action.
- For multi-tenant systems: require and verify tenant scope on every resource access.
- Avoid “existence leaks” where it matters (distinguish `404` vs `403` intentionally).

## Input Validation

- Treat all external inputs as `unknown` and decode once at the edge (body, params, headers, env, messages).
- Validate IDs, enums, timestamps, and money amounts; reject unexpected fields if the boundary is strict.

## Injection and Interpreter Boundaries

- SQL: parameterized queries (prepared statements / ORM); forbid string concatenation.
- Shell: avoid invoking a shell; pass arguments as an array; validate paths.
- Templates: avoid untrusted template evaluation; escape output; don’t allow arbitrary expressions.

## SSRF and Outbound Requests

- Only fetch from a small allowlist of hosts/schemes; validate DNS + resolved IP ranges.
- Block redirects (or re-validate after redirects) when fetching server-side.

## Secrets and Sensitive Data

- Never log secrets/tokens; don’t include them in error messages.
- Store secrets outside source control; rotate on leak suspicion; prefer short-lived credentials.

## Observability and Privacy

- Logs: whitelist safe fields; redact/omit sensitive fields; avoid raw headers/body dumps.
- Metrics: no PII in labels; keep label cardinality bounded.
- Traces: avoid raw payload attributes; prefer IDs with policy approval.

## Supply Chain / Dependencies

- Keep lockfiles; pin versions; remove unused deps.
- Prefer well-maintained libraries; verify licensing/policy constraints in your org.

