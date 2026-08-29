"""Append-only JSONL event store with monotone sequence numbers."""

from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock
from typing import Any

from scoresymphony_agent.events.models import Event


class EventStore:
    def __init__(self, state_dir: Path) -> None:
        self.path = state_dir / "events" / "events.jsonl"
        self._lock = Lock()

    def append(self, *, event_type: str, component: str, result: str, **kwargs: Any) -> Event:
        with self._lock:
            event = Event.new(
                sequence=self._next_sequence(),
                event_type=event_type,
                component=component,
                result=result,
                **kwargs,
            )
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(json.dumps(event.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            return event

    def list(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]

    def _next_sequence(self) -> int:
        events = self.list()
        return int(events[-1]["sequence"]) + 1 if events else 1
