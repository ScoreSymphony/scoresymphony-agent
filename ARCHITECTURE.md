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

## Binding KVM 4 service topology

The deployment target is fixed in [`COMPONENTS.md`](COMPONENTS.md) and [`docs/KVM4_TARGET_STACK.md`](docs/KVM4_TARGET_STACK.md).

Permanent container services are:

```text
Traefik
Authelia
PostgreSQL
ScoreSymphony Agent
Prometheus
node_exporter
```

Only Traefik exposes public HTTP/HTTPS. SSH remains a host-admin path. No other permanent service is publicly bound. The target exposure contract is maintained in [`docs/PORT_SERVICE_REGISTRY.md`](docs/PORT_SERVICE_REGISTRY.md).

Permanent-service additions or replacements that change ingress, authentication, canonical persistence, orchestration, worker execution, independent review, metrics history, backup/recovery or private worker transport require an explicit ADR.

## Human Control Plane

The primary UI contains Overview, Proposals, Specifications, Tasks, Runs, Reviews, Approvals and a read-mostly System surface. The UI renders projections from the Runtime API. It never owns task/review/approval state.

## Runtime truth

V1 uses a file-backed snapshot behind `StateStore`:

```text
state.json    materialized state
events.jsonl append-only event history
```

The V1 adapter is intentionally replaceable. PostgreSQL is present in the KVM 4 target stack for infrastructure/application persistence, beginning with authentication storage, but it is not a second Agent Task/Run/Review/Lease source of truth. A PostgreSQL-backed Agent StateStore requires a separate storage ADR and migration contract.

## Deployment boundary

The first production image is one deployable application built in two stages: React/Vite produces static assets, then FastAPI serves the API and frontend. Persistent paths are mounted outside the image. Reverse proxy, TLS, firewall, secrets and host administration remain Server Infrastructure responsibilities.

## Authentication

Development may use an explicit local principal mode. Production uses the Traefik -> Authelia ForwardAuth path. The Agent API performs its own server-side role mapping and authorization after authentication. Required logical roles are `OWNER`, `ADMIN` and `READ_ONLY`.

Production must fail closed when the trusted proxy/authentication contract is absent or invalid. Direct internet exposure of the Agent API is forbidden.

## Worker boundary

Workers implement stable adapter contracts. The core must not assume a specific model/provider. Worker categories are deterministic tools, local/GPU coding worker, FCC implementation path, FCC Codex review path and research runner.

Execution workers are run-scoped rather than permanent always-on services. Remote workers such as the KVM 8 or an ephemeral Hostinger GPU remain subordinate to the KVM 4 control plane and connect over the private worker transport.

## Review boundary

Review is independent from implementation. `approved`, `changes_requested` and `blocked` are structured outcomes. Technical transport/schema failures are never approvals.

## System surface

The UI may display host/resource/service data from explicit read-only adapters. Prometheus is the internal metrics store/query surface and node_exporter provides host metrics. Grafana is deliberately not part of the user-facing baseline because ScoreSymphony owns the System view.

The System view must not become a privileged VPS admin UI.
