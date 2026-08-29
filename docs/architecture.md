# Architecture

## Purpose

`scoresymphony-agent` is the standalone control application for ScoreSymphony agent workflows. It stays provider-neutral and starts as one Docker container.

## Runtime flow

Task → persisted state/event → run/attempt → worker adapter → deterministic evidence/tools → reviewer adapter → structured review → terminal or blocked state.

## Boundaries

- `tasks/`: task state and lifecycle data.
- `runs/`: runs and attempts.
- `state/`: persistence primitives only.
- `events/`: append-only audit events.
- `workspaces/`: workspace/worktree contract; Git-specific lifecycle is not yet implemented.
- `tools/`: deterministic, explicitly registered tools; no arbitrary shell surface.
- `workers/`: provider-neutral implementation-worker contract.
- `reviews/`: independent reviewer contract and fail-closed review validation.
- `policies/`: deny-by-default authorization decisions.
- `api/`: HTTP boundary.

## Deliberately deferred

Real FCC, Codex, Hermes, Qwen, Graphify, Git worktree automation, PostgreSQL, additional containers, production deployment automation, and external network exposure are not implemented by this bootstrap.

## Container strategy

Start with one application container and one persistent state volume. Split a runner or database into separate containers only when isolation or persistence requirements justify it.
