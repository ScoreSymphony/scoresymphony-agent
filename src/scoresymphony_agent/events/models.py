"""Append-only runtime event model."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from scoresymphony_agent.ids import make_id, utc_now


@dataclass(slots=True)
class Event:
    event_id: str
    sequence: int
    event_type: str
    component: str
    result: str
    task_id: str | None = None
    run_id: str | None = None
    attempt_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now)
    schema_version: int = 1

    @classmethod
    def new(cls, *, sequence: int, event_type: str, component: str, result: str, **kwargs: Any) -> Event:
        return cls(
            event_id=make_id("EVENT"),
            sequence=sequence,
            event_type=event_type,
            component=component,
            result=result,
            **kwargs,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
