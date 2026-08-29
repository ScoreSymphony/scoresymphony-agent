"""File-backed run store."""

from __future__ import annotations

from pathlib import Path

from scoresymphony_agent.runs.models import Run
from scoresymphony_agent.state.atomic import read_json, write_json_atomic


class RunStore:
    def __init__(self, state_dir: Path) -> None:
        self.root = state_dir / "runs"

    def save(self, run: Run, *, create_only: bool = False) -> Run:
        write_json_atomic(self._path(run.run_id), run.to_dict(), create_only=create_only)
        return run

    def get(self, run_id: str) -> Run:
        path = self._path(run_id)
        if not path.is_file():
            raise KeyError(run_id)
        return Run.from_dict(read_json(path))

    def list_for_task(self, task_id: str) -> list[Run]:
        if not self.root.exists():
            return []
        runs = [Run.from_dict(read_json(path)) for path in self.root.glob("*.json")]
        return [run for run in runs if run.task_id == task_id]

    def _path(self, run_id: str) -> Path:
        if not run_id.startswith("SCORESYMPHONY-RUN-") or "/" in run_id or "\\" in run_id:
            raise ValueError("Invalid run_id")
        return self.root / f"{run_id}.json"
