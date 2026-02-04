# Audit logging

## Intent
Record an append-only trail of security-sensitive actions for accountability and compliance.

## Use when
- You need to answer “who did what, when, and why” for privileged or sensitive operations.
- You need compliance evidence and tamper-resistance expectations.

## Avoid / watch-outs
- Don’t log secrets; minimize PII and follow retention policies.
- Audit logs should be append-only and durable; treat them as a security boundary.

## Skill mapping
- `security`: define what actions must be audited and what data is allowed.
- `observability`: implement structured audit events with correlation IDs and retention discipline.
- `spec`: document audited actions and guarantees (durability, access controls).
