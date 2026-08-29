from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from scoresymphony_agent.api.app import create_app
from scoresymphony_agent.config import Settings


def test_health_and_task_api(tmp_path: Path) -> None:
    client = TestClient(create_app(Settings(state_dir=tmp_path, environment="test")))
    assert client.get("/healthz").json() == {"status": "ok"}
    response = client.post("/v1/tasks", json={"title": "API task", "risk": "low"})
    assert response.status_code == 201
    task_id = response.json()["task_id"]
    assert client.get(f"/v1/tasks/{task_id}").status_code == 200
