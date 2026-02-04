# Exception tracking

## Intent
Capture and triage unexpected errors (exceptions) with enough context to debug and prioritize fixes.

## Use when
- You need visibility into unknown failures beyond “expected” error codes.
- You want alerting/triage workflows for regressions and hot spots.

## Avoid / watch-outs
- Avoid leaking secrets/PII in exception payloads.
- Don’t treat exception tracking as a substitute for structured errors and metrics.

## Skill mapping
- `observability`: integrate exception tracking and ensure correlation with trace/log IDs.
- `security`: enforce redaction/sanitization for captured context.
