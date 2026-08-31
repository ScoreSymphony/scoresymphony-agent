# ScoreSymphony Agent

ScoreSymphony Agent is the persistent Agent Platform and Human Control Plane for ScoreSymphony development and research.

This repository is designed from the target operating model backwards: API, Develop Control UI, state boundary, worker/review adapter boundaries, Docker deployment and tests live together from the beginning.

## Target surface

The Develop Control UI exposes:

- Overview
- Proposals
- Specifications
- Tasks
- Runs
- Reviews
- Approvals
- System (read-mostly)

The UI is never a second source of truth. Every mutation must go through the runtime command/API boundary.

## Fixed stack

- Python 3.12
- FastAPI + Pydantic
- React + TypeScript + Vite
- one production image that serves the API and built frontend
- file-backed Shared Task State V1 behind a storage interface
- Docker Compose for the first KVM-4 deployment
- pytest plus frontend typecheck/build in CI

Worker systems such as FCC, Codex review, Qwen GPU workers, research runners and code-intelligence services integrate through adapter boundaries. They are not hard-wired into the core.

## Backend

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
uvicorn scoresymphony_agent.app:app --reload --port 8080
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api` to the backend on port 8080.

## Docker

```bash
docker compose build
docker compose up -d
curl http://127.0.0.1:8080/api/v1/health
```

The Compose baseline binds the application to localhost. Public exposure, TLS and production authentication remain explicit infrastructure decisions.

See `AGENTS.md`, `ARCHITECTURE.md`, `CURRENT_STATE.md` and `docs/END_STATE.md` before changing platform boundaries.
