# Publish events using database triggers

## Intent
Use database triggers to capture changes and publish events (or write to an outbox) without changing application code.

## Use when
- You need to publish events for legacy apps where code changes are difficult.
- DB-level enforcement is an acceptable part of your operational model.

## Avoid / watch-outs
- Triggers are hard to test and debug; operational surprises are common.
- Keep the trigger logic small; prefer writing to an outbox rather than doing network I/O in triggers.

## Skill mapping
- `architecture`: evaluate trigger-based publication vs outbox/CDC for your context.
- `testing`: add end-to-end verification that DB changes imply expected events.
- `observability`: monitor trigger failures and event publication lag/backlog.
