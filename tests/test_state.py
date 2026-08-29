from __future__ import annotations

from pathlib import Path

from scoresymphony_agent.state.atomic import read_json, write_json_atomic


def test_atomic_json_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "state" / "example.json"
    write_json_atomic(path, {"schema_version": 1, "value": "ok"})
    assert read_json(path)["value"] == "ok"


def test_atomic_create_only_fails_when_file_exists(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    write_json_atomic(path, {"value": 1}, create_only=True)
    try:
        write_json_atomic(path, {"value": 2}, create_only=True)
    except FileExistsError:
        pass
    else:
        raise AssertionError("create_only must not overwrite existing files")
