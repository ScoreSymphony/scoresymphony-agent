# ScoreSymphony Agent — Component Registry

Status: CANONICAL_TARGET_COMPONENTS

This registry fixes the target component set for the KVM 4 deployment. New permanent services require an explicit architecture decision; they are not added ad hoc during implementation.

## Permanent KVM 4 host components

| Component | Decision | Role | Runtime boundary |
|---|---|---|---|
| Ubuntu 24.04 LTS | REQUIRED | host OS | Server Infrastructure |
| systemd | REQUIRED | host lifecycle, timers, recovery hooks | Server Infrastructure |
| Docker Engine | REQUIRED | container runtime | Server Infrastructure |
| Docker Compose | REQUIRED | declarative service topology | Server Infrastructure |
| Git | REQUIRED | repository/source control tooling | Server Infrastructure / Runtime tool |
| host firewall + provider firewall | REQUIRED | ingress/egress boundary | Server Infrastructure |
| fail2ban | REQUIRED | SSH abuse protection | Server Infrastructure |
| SOPS + age | REQUIRED | encrypted configuration/secret material workflow | Server Infrastructure |
| restic | REQUIRED | encrypted backup/restore engine | Server Infrastructure |
| WireGuard | REQUIRED | private remote-worker transport | Server Infrastructure |

## Permanent KVM 4 container services

| Service | Decision | Role | Public exposure |
|---|---|---|---|
| Traefik 3.7 series | REQUIRED | reverse proxy, TLS, routing | 80/443 only |
| Authelia 4.x | REQUIRED | human login, 2FA, ForwardAuth | through Traefik only |
| PostgreSQL 18 | REQUIRED | Authelia persistent storage; reserved future structured persistence | none |
| ScoreSymphony Agent | REQUIRED | Develop Control UI + API + Agent Platform Core | through Traefik only |
| Prometheus | REQUIRED | internal metrics store/query API for System view and resource evidence | none |
| node_exporter | REQUIRED | read-only host metrics source | none |

No other permanent application service is part of the baseline.

## Inside the ScoreSymphony Agent application

The deployable `scoresymphony-agent` image contains:

- React + TypeScript + Vite Develop Control UI;
- FastAPI/Pydantic Command/Query API;
- Human Principal/AuthZ boundary;
- Proposal and Specification domain;
- Task Graph and readiness projections;
- Runs and Attempts;
- Shared Task State and append-only events;
- Hermes orchestration boundary;
- Task Router;
- Resource Scheduler;
- Workspace/Worktree Manager;
- Artifact/Evidence Store;
- deterministic test/gate interfaces;
- Review Loop Manager;
- adapter registry for workers, review, research, code intelligence and telemetry.

These capabilities are one product/runtime boundary. They must not be reimplemented by server infrastructure.

## Runtime state decision

V1 canonical runtime state remains:

```text
state.json
+ events.jsonl
+ State Coordinator / Single Writer
```

PostgreSQL is deliberately **not** a second Task/Review/Lease source of truth. A PostgreSQL-backed agent state adapter requires a later explicit storage ADR and migration contract.

## On-demand execution services

These are capabilities started only for an admitted run; they are not permanent always-on services:

| Execution role | Target implementation |
|---|---|
| Deterministic runner | ScoreSymphony runner profile |
| FCC implementation | FCC Implementation Path |
| Independent review | FCC Codex Review Path, read-only review profile |
| Local coding worker | Qwen Code/local runtime only when host eligibility is proven |
| Research execution | isolated Research Runner |
| Evaluation | isolated Eval Runner |

## Remote worker services

Remote workers use the same worker protocol and never become a second control plane.

Planned examples:

- KVM 8 worker/benchmark host;
- ephemeral Hostinger GPU worker;
- Qwen3-Coder-Next-FP8/vLLM GPU service when explicitly started.

Remote connectivity uses the private worker transport. Only the KVM 4 owns canonical task/run/review state.

## Explicit exclusions

The following are not part of the baseline and must not be installed merely for convenience:

- Coolify;
- Portainer;
- Dockge;
- Kubernetes;
- Redis;
- Celery;
- RabbitMQ;
- Kafka;
- Grafana;
- Loki;
- n8n;
- Nextcloud;
- Ollama;
- a second reverse proxy;
- a second orchestrator;
- a second review loop;
- a second task-state system.

If a concrete measured gap later justifies one of these capabilities, it requires an explicit decision instead of silently expanding the stack.
