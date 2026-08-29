# Architecture

## Purpose

`scoresymphony-agent` is the standalone control application for ScoreSymphony agent workflows. It stays provider-neutral and starts as one Docker container.

## Runtime flow

Task → persisted state/event → run/attempt → worker adapter → deterministic evidence/tools → reviewer adapter → persisted structured review → terminal or blocked state.

## Boundaries

- `tasks/`: task state and lifecycle data.
- `runs/`: runs, attempts and persisted worker evidence summaries.
- `state/`: persistence primitives only.
- `events/`: append-only audit events.
- `workspaces/`: workspace/worktree contract; Git-specific lifecycle is not yet implemented.
- `tools/`: deterministic, explicitly registered tools; no arbitrary shell surface.
- `workers/`: provider-neutral implementation-worker contract.
- `reviews/`: independent reviewer contract, persistence and fail-closed review validation.
- `policies/`: deny-by-default authorization decisions.
- `api/`: HTTP boundary.

## Persistence baseline

Version 1 is deliberately file-backed. Task, run and review documents use atomic replacement. Runtime events are append-only JSONL with monotone sequence numbers for the initial single-process deployment. A database is not required to run the bootstrap.

## Safety baseline

- Critical tasks do not enter the autonomous mock execution path.
- Tools are denied unless explicitly registered for an access profile.
- Worker and reviewer interfaces are separate.
- The container runs as a non-root user, drops Linux capabilities, uses `no-new-privileges`, and keeps the root filesystem read-only in Compose.
- The default Compose binding is loopback-only; public exposure is not configured.

## Deliberately deferred

Real FCC, Codex, Hermes, Qwen, Graphify, Git worktree automation, PostgreSQL, additional containers, production deployment automation, and external network exposure are not implemented by this bootstrap.

## Container strategy

Start with one application container and one persistent state volume. Split a runner or database into separate containers only when isolation or persistence requirements justify it.
