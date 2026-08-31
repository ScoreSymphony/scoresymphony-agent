# API Contract

Base path: `/api/v1`

Current bootstrap queries:

- `GET /health`
- `GET /dashboard`
- `GET /proposals`
- `GET /specifications`
- `GET /tasks`
- `GET /runs`
- `GET /reviews`
- `GET /approvals`
- `GET /system`

Future mutations must use command endpoints and carry principal identity, command identity, expected revision and object/version binding where applicable.

Direct UI writes to `state.json`, events or worker state are forbidden.
