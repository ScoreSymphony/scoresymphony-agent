from __future__ import annotations

from abc import ABC, abstractmethod
import json
import os
from pathlib import Path
import tempfile

from scoresymphony_agent.domain import PlatformSnapshot


class StateStore(ABC):
    @abstractmethod
    def load(self) -> PlatformSnapshot:
        raise NotImplementedError

    @abstractmethod
    def save(self, snapshot: PlatformSnapshot) -> None:
        raise NotImplementedError


class JsonStateStore(StateStore):
    def __init__(self, root: Path) -> None:
        self.root = root
        self.path = root / "state.json"

    def load(self) -> PlatformSnapshot:
        if not self.path.exists():
            return PlatformSnapshot()
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return PlatformSnapshot.model_validate(data)

    def save(self, snapshot: PlatformSnapshot) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        payload = snapshot.model_dump_json(indent=2)
        fd, temp_name = tempfile.mkstemp(prefix=".state-", suffix=".tmp", dir=self.root)
        temp_path = Path(temp_name)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(payload)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, self.path)
        finally:
            temp_path.unlink(missing_ok=True)
