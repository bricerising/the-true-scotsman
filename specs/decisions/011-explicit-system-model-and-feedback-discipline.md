# Decision 011: Make System Model + Feedback Discipline Explicit

**Date**: 2026-02-06
**Status**: Accepted

## Context

The skill library already guides architecture, resilience, observability, and verification well, but several systemic-thinking behaviors are still implicit:

- Problem models are often held in the operator's head instead of externalized.
- Trade-offs are discussed but not always captured as comparable options with reversal triggers.
- Metrics are specified, but metric-to-decision linkage and review rituals are not consistently required.
- Second-order effects, blast radius, and system dynamics (delay/accumulation/drift) are not explicit enough.
- Outputs are optimized for engineers but not consistently translated for decision stakeholders.

This creates risk of locally strong decisions that are hard to align, review, and adapt over time.

## Decision

Update core workflow/spec/architecture/observability/plan/finish guidance to require lightweight explicit artifacts for non-trivial work:

1. **System sketch**: boundary, time horizon, actors/incentives, key flows, and top constraints.
2. **Decision table**: options, objectives, known downsides, and kill/reversal criteria.
3. **Measurement ladder**: decision, leading indicators, lagging outcomes, instrumentation source, review ritual/owner.
4. **Failure propagation map**: what breaks next, what breaks silently, and organizational cascade points.
5. **Dynamics check**: what accumulates, expected delays, and balancing loops.
6. **Stakeholder translation**: concise executive packet plus engineering packet for non-trivial delivery reports.

Keep these artifacts minimal and mostly template-driven to avoid skill bloat.

## Consequences

- Positive:
  - More testable and portable system models across teams and agents.
  - Clearer trade-off memory and reversibility discipline.
  - Faster learning loops by connecting telemetry to named decisions and rituals.
  - Better cross-functional alignment with dual-bandwidth reporting.
- Trade-offs:
  - Slightly higher upfront structure for non-trivial work.
  - More template maintenance across skills and prompt recipes.
- Compatibility/migration impact:
  - Additive change only; no skill renames or taxonomy changes.
  - Existing prompts remain valid and can adopt new artifacts incrementally.
