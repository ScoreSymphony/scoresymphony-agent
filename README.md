# ScoreSymphony Agent

`ScoreSymphony Agent` is the standalone agent application for coordinating tasks, runs, state, workspaces, tools, workers, reviews, policies, and later API/UI access around ScoreSymphony development workflows.

## Bootstrap status

This repository currently contains the minimal application skeleton only. It does not yet provide production-ready agent orchestration, autonomous coding, deployment, or VPS administration.

## Initial layout

- `src/scoresymphony_agent/` – Python application core
- `frontend/` – future web interface
- `config/` – non-secret configuration templates
- `schemas/` – machine-readable contracts
- `tests/` – automated tests
- `docs/` – architecture and operating documentation
- `Dockerfile` / `compose.yaml` – minimal container packaging

## Principles

- keep the first version small and deterministic
- do not duplicate ScoreSymphony product logic
- isolate workers and permissions only when concrete requirements justify it
- keep secrets out of Git
- prefer one application and one container initially
- add services such as PostgreSQL only when a real dependency exists

## Local development

```bash
python -m venv .venv
python -m pip install -e .
scoresymphony-agent status
```

## Docker

```bash
docker compose build
docker compose run --rm scoresymphony-agent status
```
