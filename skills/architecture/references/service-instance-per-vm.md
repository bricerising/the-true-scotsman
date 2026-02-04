# Service Instance per VM

## Intent
Run each service instance in its own VM to increase isolation and reduce cross-service interference.

## Use when
- Stronger isolation is required (security, compliance, noisy-neighbor risk).
- Your platform and operational model are VM-first (or containers are not acceptable).

## Avoid / watch-outs
- VM lifecycle and scaling is often slower/heavier than containers.
- Ensure consistent provisioning and golden images to avoid drift.

## Skill mapping
- `architecture`: document isolation and scaling trade-offs for the chosen runtime.
- `platform`: standardize provisioning and per-service runtime defaults.
