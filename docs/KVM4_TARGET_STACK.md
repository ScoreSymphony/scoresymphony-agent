# KVM 4 Target Stack

Status: BINDING_TARGET_TOPOLOGY

This document defines the end-state service topology used to drive implementation and deployment. The implementation may be incomplete, but the service boundaries do not change implicitly from work package to work package.

## Target topology

```text
INTERNET
   |
   +-- TCP 80/443
   v
Traefik
   |
   +--> Authelia authentication / 2FA
   |
   +--> ScoreSymphony Agent
           |
           +-- Develop Control UI
           +-- Command / Query API
           +-- Agent Platform Core
           +-- Shared Runtime State
           +-- Worker / Review adapters
           +-- System read-model
           |
           +--> Prometheus query API

PRIVATE NETWORKS
   |
   +-- PostgreSQL <--> Authelia
   +-- Prometheus  <--> node_exporter
   +-- Worker transport <--> KVM8 / ephemeral GPU workers

HOST-ONLY OPERATIONS
   |
   +-- systemd
   +-- firewall
   +-- fail2ban
   +-- restic
   +-- SOPS + age
   +-- WireGuard
```

## Permanent service count

The baseline intentionally contains six permanent application containers:

1. `traefik`
2. `authelia`
3. `postgres`
4. `scoresymphony-agent`
5. `prometheus`
6. `node-exporter`

Execution workers are run-scoped and are not added to the always-on baseline.

## Why these components are fixed

### Traefik

Owns all public HTTP/HTTPS ingress, certificate handling and routing. No second reverse proxy is deployed.

### Authelia

Owns interactive human authentication and 2FA. Traefik performs ForwardAuth and forwards an authenticated principal to the Agent API. The Agent still performs server-side authorization for mutating commands.

### PostgreSQL

Provides durable relational storage for Authelia and leaves a stable relational service available for future approved structured persistence. It does not become canonical Agent Task/Run/Review state by mere presence.

### ScoreSymphony Agent

One deployable product containing frontend and API. It is the only Develop Control Plane. It owns the Agent Platform runtime semantics.

### Prometheus

Internal metrics store and query surface. It exists so the ScoreSymphony `System` view can show resource/history data without making Grafana a second user-facing dashboard.

### node_exporter

Read-only host metrics source for Prometheus. It has no public listener.

## Network zones

Recommended logical networks:

```text
edge
  Traefik
  Authelia
  ScoreSymphony Agent

auth-db
  Authelia
  PostgreSQL

monitoring
  Prometheus
  node_exporter
  ScoreSymphony Agent (query access only)

worker-private
  host WireGuard interface / worker gateway
```

No database, metrics service or worker control endpoint is publicly exposed.

## Public ports

Only the following public ports belong to the baseline:

| Port | Protocol | Owner | Purpose |
|---:|---|---|---|
| 22 | TCP | host SSH | owner/admin access |
| 80 | TCP | Traefik | HTTP -> HTTPS / ACME as required |
| 443 | TCP | Traefik | Develop Control UI/API + auth portal |

WireGuard receives a dedicated UDP port only when the private worker network is activated. The exact port is infrastructure configuration, not an Agent API contract.

## Internal ports

| Service | Default internal port | Exposure |
|---|---:|---|
| ScoreSymphony Agent | 8080 | container networks only |
| Authelia | 9091 | container networks only |
| PostgreSQL | 5432 | `auth-db` only |
| Prometheus | 9090 | `monitoring` only |
| node_exporter | 9100 | `monitoring` only |

## Human authentication flow

```text
Browser
  -> Traefik
  -> Authelia ForwardAuth
  -> authenticated principal/groups
  -> ScoreSymphony Agent
  -> server-side role mapping
  -> Query or Command
```

Required logical Agent roles remain:

- `OWNER`
- `ADMIN`
- `READ_ONLY`

A reverse-proxy authentication success never authorizes a command by itself. The API validates the principal and role for the target action.

## Runtime state

Canonical V1 Agent state:

```text
/var/lib/scoresymphony-agent/
  state.json
  events.jsonl
  artifacts/
  checkpoints/
```

The storage implementation stays behind interfaces so a later approved migration does not change API or domain contracts.

## Persistent server data

```text
/var/lib/scoresymphony-agent/      Agent runtime state
/srv/scoresymphony-artifacts/     large run/evidence artifacts
/srv/scoresymphony/worktrees/     task/review worktrees
/var/lib/postgresql/              PostgreSQL-managed data
/etc/scoresymphony/               non-secret host/runtime configuration
/etc/scoresymphony/credentials.d/ decrypted runtime secrets, root controlled
/var/backups/scoresymphony/       local staging area for backup jobs
```

Exact distribution-managed PostgreSQL paths may differ and are discovered at deployment time rather than hard-coded into Agent logic.

## Backup target

`restic` is the backup engine. The preferred no-new-recurring-cost disaster-recovery target is another already-owned host (for example the second VPS) once that backup trust path is configured. GitHub remains the remote source for versioned code but is not a substitute for runtime-state/database backup.

## Remote workers

The KVM 4 remains the control plane even when computation moves elsewhere:

```text
KVM 4 Agent Platform
   |
   +-- private authenticated worker protocol
           |
           +--> KVM 8 worker
           +--> Hostinger GPU worker
                   Qwen3-Coder-Next-FP8 + vLLM
```

Remote workers receive scoped tasks and return events/artifacts/results. They do not own canonical scheduling, approvals or review state.

## Deliberately absent

The target does not use Portainer, Coolify, Dockge or Grafana as primary interfaces. The user-facing operational surface is the ScoreSymphony Develop Control UI. Privileged host administration stays separate in the host/provider trust domain.

There is no Redis/Celery baseline. Durable task/run orchestration belongs to the Agent Platform rather than a parallel queue architecture.

## Change rule

A permanent-service addition or replacement is architecture-significant when it changes one of these responsibilities:

- public ingress;
- authentication;
- canonical persistence;
- orchestration;
- worker execution;
- independent review;
- metrics history;
- backup/recovery;
- private worker transport.

Such a change requires an explicit ADR and must not happen as an incidental implementation choice.
