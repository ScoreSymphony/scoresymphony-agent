# scoresymphony-agent

Standalone, provider-neutral control application for ScoreSymphony agent workflows.

## Current scope

The repository now provides the executable foundation for:

- tasks with risk, scope and acceptance criteria;
- file-backed atomic state;
- append-only event history;
- runs and attempts with persisted worker summaries, changed files and claims;
- persisted structured reviews linked to task/run/attempt/reviewer identities;
- model/provider-neutral worker and reviewer contracts;
- fail-closed structured review validation;
- deny-by-default deterministic tool authorization;
- HTTP API and CLI;
- a deterministic mock end-to-end loop for development tests;
- one-container Docker/Compose deployment shape;
- CI tests, linting and Docker build validation.

It intentionally does **not** yet contain real FCC, Codex, Hermes, Qwen, Graphify, PostgreSQL, Git worktree automation or production deployment logic.

## Local development

```bash
python -m venv .venv
# Activate the environment for your shell.
python -m pip install -e ".[dev]"
pytest -q
ruff check .
```

Create and inspect tasks:

```bash
scoresymphony-agent task create "Example task" --risk low
scoresymphony-agent task list
scoresymphony-agent status
```

Start the API:

```bash
scoresymphony-agent serve
```

Endpoints include:

- `GET /healthz`
- `GET /v1/status`
- `GET/POST /v1/tasks`
- `GET /v1/tasks/{task_id}`
- `GET /v1/tasks/{task_id}/runs`
- `GET /v1/runs/{run_id}/reviews`

## Docker

```bash
docker compose up --build
```

The Compose file binds the API to `127.0.0.1:8000` by default and persists state in a named volume. It does not expose the service publicly.

## Design rule

Keep the first deployment simple: one repository, one Compose project, one application container. Add separate runner/database/model containers only when an actual isolation or persistence requirement appears.

See `docs/architecture.md` and `docs/adapter-roadmap.md`.
