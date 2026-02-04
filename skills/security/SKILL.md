---
name: security
description: Apply security guardrails for enterprise web apps (authn/authz, input validation, injection prevention, secrets, secure logging, SSRF, dependency hygiene). Use when adding or changing endpoints, auth flows, data access, file/network I/O, or handling sensitive data.
---

# Security

## Overview

Security is boundary discipline: authenticate, authorize, validate inputs, avoid data leakage, and make unsafe classes of bugs hard to write.

This is not a full security audit. If the change is high-risk (auth overhaul, multi-tenant isolation, crypto, payments, regulated data), escalate to a security review.

## Workflow

1. Identify what changed (the *attack surface*):
   - inbound boundaries: HTTP/gRPC/GraphQL/WS handlers, webhooks
   - outbound boundaries: HTTP/gRPC/SDK clients, redirects, proxying, fetch-by-URL
   - state boundaries: DB queries, object storage, caches, queues
   - operational boundaries: logs/telemetry, admin endpoints, config/secrets
2. Classify data sensitivity:
   - credentials/secrets, session tokens, API keys
   - PII and regulated data
   - multi-tenant identifiers and access scopes
3. Apply baseline controls:
   1. **Authn**: verify identity and token validity (issuer/audience/expiry).
   2. **Authz**: check permissions *per action* (and per tenant/resource).
   3. **Input validation**: treat external inputs as `unknown`; decode/validate at the edge.
   4. **Injection safety**: parameterize queries; avoid string-built interpreters (SQL, shell, template injection).
   5. **Secrets safety**: keep secrets out of logs, error messages, and client responses.
4. Harden outbound calls:
   - SSRF controls (allowlist hosts; block link-local/metadata IPs; disable redirect-follow where unsafe)
   - TLS verification and timeouts/cancellation (see `resilience`)
5. Verify:
   - add/extend consumer-visible tests for authz and validation (`testing`)
   - run any available dependency scanning / linters in the target repo
   - sanity-check logs/metrics do not include sensitive fields (`observability`)

## Checklist (High-Signal)

- Authn: token validation, session/cookie settings, CSRF (if cookie-based), re-auth for sensitive actions.
- Authz: resource/tenant checks at every entrypoint; no “UI-only” authorization.
- Inputs: strict decoding; file uploads have size/type limits; URLs are parsed and validated.
- DB: parameterized queries; least-privilege DB user; no leaking of existence via error detail (where relevant).
- Secrets: never log credentials; rotate/expire tokens; store secrets in secret manager/env (not source).
- Telemetry: logs redact/omit PII; metrics have bounded labels; traces avoid raw payloads.
- Dependencies: pin and update; remove unused; verify integrity/lockfiles.

## Guardrails

- Don’t build your own crypto; use well-reviewed libraries and platform primitives.
- Don’t weaken authz “temporarily”; if you must, add explicit expiry and a follow-up task.
- Don’t log raw request bodies/headers by default; explicitly whitelist safe fields.
- Don’t accept user-provided URLs for server-side fetch without SSRF controls.

## References

- Deeper checklist: [`references/checklists.md`](references/checklists.md)
- Boundary resiliency: [`resilience`](../resilience/SKILL.md)
- Telemetry privacy: [`observability`](../observability/SKILL.md)
- Consumer-visible verification: [`testing`](../testing/SKILL.md)
- Shared auth/config primitives (when 2+ services need the same guardrails): [`platform`](../platform/SKILL.md)

## Output Template

When applying this skill, return:

- What changed (attack surface) and what data is sensitive.
- The controls applied (authn/authz/validation/injection/SSRF/logging).
- Verification steps (tests + local checks) and any follow-ups needing a dedicated security review.
