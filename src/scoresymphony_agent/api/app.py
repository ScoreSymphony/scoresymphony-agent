"""HTTP API for the single-container ScoreSymphony Agent application."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from scoresymphony_agent import __version__
from scoresymphony_agent.config import Settings
from scoresymphony_agent.runtime import AgentRuntime
from scoresymphony_agent.tasks.models import RiskClass


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    risk: RiskClass = RiskClass.LOW
    scope: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    runtime = AgentRuntime(settings.state_dir)
    app = FastAPI(title="ScoreSymphony Agent", version=__version__)

    @app.get("/")
    def root() -> dict[str, str]:
        return {"service": "scoresymphony-agent", "status": "ready"}

    @app.get("/healthz")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/v1/status")
    def status() -> dict[str, str]:
        return {
            "service": "scoresymphony-agent",
            "version": __version__,
            "environment": settings.environment,
        }

    @app.post("/v1/tasks", status_code=201)
    def create_task(payload: TaskCreate) -> dict:
        task = runtime.create_task(
            payload.title,
            description=payload.description,
            risk=payload.risk,
            scope=payload.scope,
            acceptance_criteria=payload.acceptance_criteria,
        )
        return task.to_dict()

    @app.get("/v1/tasks")
    def list_tasks() -> list[dict]:
        return [task.to_dict() for task in runtime.tasks.list()]

    @app.get("/v1/tasks/{task_id}")
    def get_task(task_id: str) -> dict:
        try:
            return runtime.tasks.get(task_id).to_dict()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Task not found") from exc
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid task id") from exc

    return app


app = create_app()
