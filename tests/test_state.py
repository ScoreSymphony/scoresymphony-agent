from pathlib import Path

from scoresymphony_agent.domain import PlatformSnapshot
from scoresymphony_agent.state import JsonStateStore


def test_json_state_store_roundtrip(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path / "state")
    snapshot = PlatformSnapshot(state_revision=7, last_event_sequence=12)
    store.save(snapshot)
    loaded = store.load()
    assert loaded.state_revision == 7
    assert loaded.last_event_sequence == 12
    assert (tmp_path / "state" / "state.json").exists()
