# AGENTS.md

## Scope

This repository owns the ScoreSymphony Agent Platform: Human Control Plane, runtime contracts, state coordination, orchestration, worker/review adapters and the Develop Control UI.

It does not own host administration or ScoreSymphony music-product logic.

## Hard rules

1. Never treat `main` as an agent development branch.
2. Never give runtime agents implicit sudo, host-admin, Docker-root-socket or main-merge authority.
3. The UI must not write canonical state directly. Mutations go through commands/APIs and policy checks.
4. Shared Task State has one canonical mutation path. Storage adapters may change; state semantics may not fork.
5. Codex review remains read-only relative to the reviewed source.
6. FCC implementation and FCC/Codex review are separate trust paths even when hosted by one execution platform.
7. Deterministic checks precede LLM judgement whenever possible.
8. A process exit code of zero is not sufficient evidence of task success.
9. Missing or invalid mandatory evidence fails closed.
10. Do not persist secrets in Git, state, logs, reviews or artifacts.
11. Do not introduce paid-provider fallback paths implicitly.
12. Do not add a second orchestrator, task state, review loop or worktree authority.
13. External workers, models, skills and services integrate through explicit adapter/capability boundaries.
14. Infrastructure-specific host actions belong outside this repository.

## Status language

Use `IMPLEMENTED`, `PARTIALLY_IMPLEMENTED`, `PREPARED`, `PLANNED`, `OPTIONAL`, `UNVERIFIED`, `BLOCKED` and `SUPERSEDED` only when evidence supports the claim.
