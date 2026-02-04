# Access token

## Intent
Propagate authentication/authorization context between services using an access token (e.g., JWT).

## Use when
- Services need to verify the caller’s identity/scopes (end user or service principal).
- You need consistent authn/authz decisions across multiple services and boundaries.

## Avoid / watch-outs
- Validate issuer/audience/expiry; don’t trust tokens without signature verification.
- Be careful with token forwarding across trust boundaries; avoid oversharing scopes/claims.

## Skill mapping
- `security`: token validation, authz checks, and safe logging of auth context.
- `platform`: shared auth middleware/interceptors for consistent behavior.
- `spec`: document auth expectations per endpoint/event and failure semantics.
