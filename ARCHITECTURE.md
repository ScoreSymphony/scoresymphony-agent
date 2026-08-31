# ScoreSymphony Agent — Target Architecture

Status: TARGET

## End state

```text
User
  |
  v
Develop Control UI (React)
  |
  v
FastAPI Command / Query API
  |
  +--> Human principal / AuthZ boundary
  |
  v
Agent Platform Core
  |
  +--> Proposal / Specification / Task Graph
  +--> Shared Task State + Events
  +--> Hermes orchestration boundary
  +--> Task Router
  +--> Resource Scheduler
  +--> Workspace / Worktree Manager
  +--> Artifact / Evidence Store
  +--> Test Gate adapters
  +--> Review Loop Manager
  |
  +--> FCC implementation adapter
  +--> FCC Codex review adapter (read-only)
  +--> Local/GPU worker adapter
  +--> Research runner adapter
  +--> Code-intelligence adapter
```

## Human Control Plane

The primary UI contains Overview, Proposals, Specifications, Tasks, Runs, Reviews, Approvals and a read-mostly System surface. The UI renders projections from the Runtime API. It never owns task/review/approval state.

## Runtime truth

V1 uses a file-backed snapshot behind `StateStore`:

```text
state.json    materialized state
events.jsonl append-only event history
```

The V1 adapter is intentionally replaceable. A future PostgreSQL adapter may be added after a measured concurrency/query requirement without changing domain semantics or API contracts.

## Deployment boundary

The first production image is one deployable application built in two stages: React/Vite produces static assets, then FastAPI serves the API and frontend. Persistent paths are mounted outside the image. Reverse proxy, TLS, firewall, secrets and host administration remain Server Infrastructure responsibilities.

## Authentication

Development may use an explicit local principal mode. Production must fail closed until a real authentication provider and server-side role mapping are configured. Required logical roles are `OWNER`, `ADMIN` and `READ_ONLY`.

## Worker boundary

Workers implement stable adapter contracts. The core must not assume a specific model/provider. Worker categories are deterministic tools, local/GPU coding worker, FCC implementation path, FCC Codex review path and research runner.

## Review boundary

Review is independent from implementation. `approved`, `changes_requested` and `blocked` are structured outcomes. Technical transport/schema failures are never approvals.

## System surface

The UI may display host/resource/service data from explicit read-only adapters. It must not become a privileged VPS admin UI.
