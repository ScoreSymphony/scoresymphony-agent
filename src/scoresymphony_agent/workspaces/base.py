"""Workspace contract. Git worktree mechanics are added behind this interface later."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class Workspace:
    task_id: str
    path: Path
    read_only: bool = False


class WorkspaceManager(Protocol):
    def acquire(self, task_id: str, *, read_only: bool = False) -> Workspace: ...

    def release(self, workspace: Workspace) -> None: ...
