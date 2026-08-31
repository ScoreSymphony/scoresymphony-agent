# KVM 4 Port and Service Registry

Status: TARGET_REGISTRY

This file is the target exposure registry for the Agent Platform deployment. `CURRENT_STATE.md` remains the source for what is actually deployed and listening.

| Service | Runtime | Port | Protocol | Bind / Network | Public | Authentication | TLS | Owner |
|---|---|---:|---|---|---|---|---|---|
| SSH | host | 22 | TCP | host | yes | SSH key / host policy | SSH | Server Infrastructure |
| Traefik HTTP | container | 80 | TCP | host | yes | n/a | redirect/ACME | Server Infrastructure |
| Traefik HTTPS | container | 443 | TCP | host | yes | Authelia + Agent AuthZ | yes | Server Infrastructure |
| ScoreSymphony Agent | container | 8080 | TCP | internal `edge` | no | trusted proxy principal + API AuthZ | internal | Agent Platform |
| Authelia | container | 9091 | TCP | internal `edge` | no direct exposure | Authelia | external TLS terminates at Traefik | Server Infrastructure |
| PostgreSQL | container/service | 5432 | TCP | internal `auth-db` | no | DB role/password | internal | Server Infrastructure |
| Prometheus | container | 9090 | TCP | internal `monitoring` | no | network + service policy | internal | Server Infrastructure |
| node_exporter | container | 9100 | TCP | internal `monitoring` | no | network isolation | internal | Server Infrastructure |
| WireGuard | host | OWNER_CONFIGURED | UDP | host | only when activated | WireGuard keys | encrypted tunnel | Server Infrastructure |

## Exposure rules

1. No service except SSH and Traefik publishes a host port in the permanent baseline.
2. The Agent API is not reachable directly from the internet.
3. Authenticated identity headers are accepted only on the trusted Traefik-to-Agent path.
4. PostgreSQL is never published to the public interface.
5. Prometheus and node_exporter are internal data sources for the ScoreSymphony System view; they are not user-facing dashboards.
6. Worker traffic uses the private worker transport and scoped runtime credentials.
7. Any new public port requires this registry, firewall rules, threat review and an explicit deployment change.
