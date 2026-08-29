"""Model/provider-neutral worker contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True, slots=True)
class WorkerRequest:
    task_id: str
    run_id: str
    attempt_id: str
    title: str
    description: str
    scope: list[str]
    acceptance_criteria: list[str]


@dataclass(frozen=True, slots=True)
class WorkerResult:
    success: bool
    exit_code: int
    summary: str
    changed_files: list[str] = field(default_factory=list)
    claims: list[str] = field(default_factory=list)


class Worker(Protocol):
    agent_id: str

    def run(self, request: WorkerRequest) -> WorkerResult: ...


class MockWorker:
    """Deterministic worker used only for tests and integration development."""

    agent_id = "scoresymphony-mock-worker"

    def run(self, request: WorkerRequest) -> WorkerResult:
        return WorkerResult(
            success=True,
            exit_code=0,
            summary=f"Mock execution completed for {request.task_id}",
        )
