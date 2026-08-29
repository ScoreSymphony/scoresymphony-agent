"""File-backed task store for the first single-container runtime."""

from __future__ import annotations

from pathlib import Path

from scoresymphony_agent.state.atomic import read_json, write_json_atomic
from scoresymphony_agent.tasks.models import Task


class TaskStore:
    def __init__(self, state_dir: Path) -> None:
        self.root = state_dir / "tasks"

    def create(self, task: Task) -> Task:
        write_json_atomic(self._path(task.task_id), task.to_dict(), create_only=True)
        return task

    def save(self, task: Task) -> Task:
        write_json_atomic(self._path(task.task_id), task.to_dict())
        return task

    def get(self, task_id: str) -> Task:
        path = self._path(task_id)
        if not path.is_file():
            raise KeyError(task_id)
        return Task.from_dict(read_json(path))

    def list(self) -> list[Task]:
        if not self.root.exists():
            return []
        return sorted(
            (Task.from_dict(read_json(path)) for path in self.root.glob("*.json")),
            key=lambda task: task.created_at,
        )

    def _path(self, task_id: str) -> Path:
        if not task_id.startswith("SCORESYMPHONY-TASK-") or "/" in task_id or "\\" in task_id:
            raise ValueError("Invalid task_id")
        return self.root / f"{task_id}.json"
