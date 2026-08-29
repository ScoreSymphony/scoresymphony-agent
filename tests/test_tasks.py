from __future__ import annotations

from pathlib import Path

from scoresymphony_agent.tasks.models import RiskClass, Task
from scoresymphony_agent.tasks.store import TaskStore


def test_task_store_roundtrip(tmp_path: Path) -> None:
    store = TaskStore(tmp_path)
    task = Task.new("Build task model", risk=RiskClass.MEDIUM, scope=["src/"])
    store.create(task)
    loaded = store.get(task.task_id)
    assert loaded.task_id == task.task_id
    assert loaded.risk is RiskClass.MEDIUM
    assert store.list()[0].title == "Build task model"
