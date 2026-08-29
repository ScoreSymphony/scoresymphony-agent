from __future__ import annotations

from pathlib import Path

from scoresymphony_agent.events.store import EventStore


def test_event_sequences_are_monotone(tmp_path: Path) -> None:
    store = EventStore(tmp_path)
    first = store.append(event_type="one", component="test", result="ok")
    second = store.append(event_type="two", component="test", result="ok")
    assert first.sequence == 1
    assert second.sequence == 2
    assert len(store.list()) == 2
