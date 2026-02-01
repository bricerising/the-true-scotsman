# Decision 005: Add a Security Hardening Skill

**Date**: 2026-02-01
**Status**: Accepted

## Context

This repo already encodes security/privacy expectations (e.g., “don’t log secrets/PII”), but it lacked a dedicated, procedural skill that prompts agents to apply common security guardrails when boundaries change.

Enterprise web apps frequently change attack surface via:

- new/changed endpoints (HTTP/gRPC/WS/webhooks)
- auth/session changes
- multi-tenant resource access
- server-side outbound requests (SSRF risk)
- file uploads and interpreter boundaries

Without an explicit security checklist, agents can produce “correct” changes that are insecure-by-default.

## Decision

Add a new skill, `apply-security-patterns`, under the **Harden** stage.

The skill is intentionally pragmatic (not an exhaustive security audit) and focuses on:

- authn/authz per action/resource/tenant
- strict boundary input validation
- injection safety at interpreter boundaries
- secrets/PII safe handling (especially in logs/telemetry)
- SSRF guardrails for outbound requests

Update the default workflow documentation and prompt recipes to include it, and add it as a default hardening step in `enterprise-web-app-workflow`.

## Consequences

- Positive: Raises baseline security hygiene for boundary changes; makes security review steps explicit and repeatable.
- Trade-off: Some overlap with resilience/observability guidance; mitigated by keeping security-specific checks focused and cross-linking rather than duplicating.
- Compatibility: Additive only (new skill + documentation updates); no renames or breaking prompt contracts.

