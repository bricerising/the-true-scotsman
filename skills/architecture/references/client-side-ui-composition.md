# Client-side UI composition

## Intent
Compose a UI in the browser by assembling data and/or UI fragments from multiple backend services.

## Use when
- You want teams to ship UI slices independently (micro-frontend style).
- The browser can safely call the required backends (auth, CORS, and performance are manageable).

## Avoid / watch-outs
- Browsers calling many services increases latency and complicates auth/token handling.
- Ensure consistent UX under partial failures (some widgets fail, page still usable).

## Skill mapping
- `architecture`: decide where composition happens (client vs server vs gateway/BFF).
- `security`: safe token handling and CORS; avoid exposing internal services directly.
- `resilience`: timeouts and degraded-mode UX requirements.
- `observability`: client → backend correlation (propagate request/trace IDs).
