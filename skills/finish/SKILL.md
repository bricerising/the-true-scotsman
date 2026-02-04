---
name: finish
description: Run a ship-quality “definition of done” pass: verify, tighten contracts/docs, and produce a crisp change summary. Use at the end of non-trivial work before calling it done.
---

# Finish

## Overview

Turn “it works on my machine” into “this is ready to ship” by running verification, checking boundary discipline, and reporting changes in a consistent format.

## Workflow

1. Re-check intent artifacts:
   - if contracts/semantics changed: specs/contracts are updated (`spec`)
   - if shared primitives were added/changed: API surface + adoption notes are clear (`platform`)
2. Run verification (prefer narrow → broad):
   - unit tests / focused tests
   - typecheck
   - lint/format (if configured)
   - build (if relevant)
3. Boundary discipline spot-check (only where the change touched boundaries):
   - timeouts/cancellation/retry safety (`resilience`)
   - authn/authz + input validation + safe logging (`security`)
   - logs/traces/metrics correlation + low-cardinality labels (`observability`)
4. Cleanup:
   - remove dead code, debug logs, commented-out blocks
   - ensure errors are actionable and don’t leak secrets/PII
   - update quickstarts or runbooks if needed

## Guardrails

- Don’t claim verification you didn’t run; report “not run” and why.
- Prefer explicit commands and outputs over vague statements (“tests passed”).
- Don’t expand scope; if you find unrelated issues, list as follow-ups.

## Output Template

Return:

- **What changed**: 3–7 bullets (behavior + contract impact).
- **Files touched**: key paths only.
- **Verification**: commands run + results (or why not run).
- **Risks/follow-ups**: anything to watch in rollout, plus next tasks.

