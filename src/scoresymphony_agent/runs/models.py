"""Run and attempt models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from scoresymphony_agent.ids import make_id, utc_now


class RunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass(slots=True)
class Attempt:
    attempt_id: str
    agent_id: str
    status: RunStatus = RunStatus.PENDING
    started_at: str | None = None
    ended_at: str | None = None
    exit_code: int | None = None
    failure_reason: str | None = None

    @classmethod
    def new(cls, agent_id: str) -> "Attempt":
        return cls(attempt_id=make_id("ATTEMPT"), agent_id=agent_id)


@dataclass(slots=True)
class Run:
    run_id: str
    task_id: str
    status: RunStatus = RunStatus.PENDING
    attempts: list[Attempt] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    schema_version: int = 1

    @classmethod
    def new(cls, task_id: str) -> "Run":
        return cls(run_id=make_id("RUN"), task_id=task_id)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Run":
        attempts = [
            Attempt(
                attempt_id=str(item["attempt_id"]),
                agent_id=str(item["agent_id"]),
                status=RunStatus(item.get("status", RunStatus.PENDING)),
                started_at=item.get("started_at"),
                ended_at=item.get("ended_at"),
                exit_code=item.get("exit_code"),
                failure_reason=item.get("failure_reason"),
            )
            for item in value.get("attempts", [])
        ]
        return cls(
            run_id=str(value["run_id"]),
            task_id=str(value["task_id"]),
            status=RunStatus(value.get("status", RunStatus.PENDING)),
            attempts=attempts,
            created_at=str(value["created_at"]),
            updated_at=str(value["updated_at"]),
            schema_version=int(value.get("schema_version", 1)),
        )
