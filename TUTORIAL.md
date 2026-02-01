# Tutorial (Example Walkthrough)

This is a concrete example of using the playbook end-to-end on a typical enterprise web app change.

## 1) Start the session (auto-route)

Copy/paste:

```text
Use enterprise-web-app-workflow (read enterprise-web-app-workflow/SKILL.md).

Task: Add a “pause subscription” endpoint that pauses billing immediately, emits an event, and is reversible by support.
Constraints: Multi-tenant. Must be auditable. No PII in logs.
```

## 2) What a “good” run looks like

The agent should (roughly) follow:

1. **Define**
   - Write/update a spec bundle with acceptance scenarios and failure-mode expectations (`spec-driven-development`).
   - If this crosses services (billing + subscriptions + notifications), pick a minimal system pattern (`select-architecture-pattern`).
2. **Standardize**
   - If multiple services need the same auth/error/timeout/telemetry policy, propose a shared primitive (`shared-platform-library`).
   - If TypeScript, apply the systemic safety rules while implementing (`typescript-style-guide`).
3. **Harden**
   - Make outbound calls time-bounded and retry/idempotency-safe (`apply-resilience-patterns`).
   - Apply authn/authz, input validation, injection safety, and SSRF/logging guardrails (`apply-security-patterns`).
   - Add correlated logs/traces/metrics with a stable field contract and local verification steps (`apply-observability-patterns`).
4. **Verify**
   - Add consumer-visible tests that pin the contract and failure semantics (`consumer-test-coverage`).
5. **Mechanics (only if needed)**
   - Use a GoF pattern only when it buys a clearer seam (e.g., a `Proxy` wrapper for a client with retries/metrics).

## 3) What to expect in the final response

At minimum:

- Skills applied (and why).
- What changed (behavior + contract impacts).
- Verification commands run (or why not) + results.
- Follow-ups (only if necessary).

## If you’re not using TypeScript

Most of the playbook is language-agnostic (contracts, boundaries, time budgets, idempotency, telemetry, tests). Translate the “TypeScript” parts into your stack’s equivalents (e.g., typed validation/decoders, explicit dependency wiring, explicit lifetimes).

