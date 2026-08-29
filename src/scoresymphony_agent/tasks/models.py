"""Task domain model."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from scoresymphony_agent.ids import make_id, utc_now


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RiskClass(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(slots=True)
class Task:
    task_id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    risk: RiskClass = RiskClass.LOW
    scope: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    schema_version: int = 1

    @classmethod
    def new(
        cls,
        title: str,
        *,
        description: str = "",
        risk: RiskClass = RiskClass.LOW,
        scope: list[str] | None = None,
        acceptance_criteria: list[str] | None = None,
    ) -> "Task":
        if not title.strip():
            raise ValueError("Task title must not be empty")
        return cls(
            task_id=make_id("TASK"),
            title=title.strip(),
            description=description.strip(),
            risk=risk,
            scope=list(scope or []),
            acceptance_criteria=list(acceptance_criteria or []),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Task":
        return cls(
            task_id=str(value["task_id"]),
            title=str(value["title"]),
            description=str(value.get("description", "")),
            status=TaskStatus(value.get("status", TaskStatus.PENDING)),
            risk=RiskClass(value.get("risk", RiskClass.LOW)),
            scope=list(value.get("scope", [])),
            acceptance_criteria=list(value.get("acceptance_criteria", [])),
            created_at=str(value["created_at"]),
            updated_at=str(value["updated_at"]),
            schema_version=int(value.get("schema_version", 1)),
        )
