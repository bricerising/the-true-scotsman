# Service per team

## Intent
Align services and their boundaries to team ownership to maximize autonomy and reduce coordination overhead.

## Use when
- You have multiple teams and want clear responsibility and on-call ownership per service.
- Organizational boundaries are stable enough to map to long-lived service boundaries.

## Avoid / watch-outs
- Don’t let org structure alone dictate the model; keep domain boundaries defensible.
- Plan for collaboration patterns when a workflow spans teams (events/sagas/contracts).

## Skill mapping
- `architecture`: define ownership boundaries, APIs/events, and cross-team workflows.
- `spec`: document contracts, SLAs/SLOs, and change/versioning process.
- `platform`: standardize shared primitives to reduce “N ways of doing auth/telemetry”.
