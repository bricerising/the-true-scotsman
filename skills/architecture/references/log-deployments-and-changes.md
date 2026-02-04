# Log deployments and changes

## Intent
Record deployments and configuration changes as events so operational signals can be correlated to changes.

## Use when
- You want to quickly answer “what changed?” when an incident starts.
- You need to correlate error/latency regressions to specific deploys or config flips.

## Avoid / watch-outs
- Ensure change events are reliable and discoverable; “best effort” change logging is often missing when you need it.
- Don’t include secrets in change events; log versions/hashes, not values.

## Skill mapping
- `observability`: emit deploy markers (sha/version) and config hashes, and wire dashboards.
- `platform`: standardize how services report version/build info.
