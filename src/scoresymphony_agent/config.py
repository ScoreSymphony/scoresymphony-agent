from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True, slots=True)
class Settings:
    environment: str
    state_root: Path
    auth_mode: str
    frontend_dir: Path

    @classmethod
    def from_env(cls) -> "Settings":
        environment = os.getenv("SCORESYMPHONY_ENV", "development")
        default_state = "/var/lib/scoresymphony-agent" if environment == "production" else "./state-local"
        auth_mode = os.getenv("SCORESYMPHONY_AUTH_MODE", "development")
        if environment == "production" and auth_mode in {"development", "disabled"}:
            raise RuntimeError("production requires an explicit authenticated principal provider")
        return cls(
            environment=environment,
            state_root=Path(os.getenv("SCORESYMPHONY_STATE_ROOT", default_state)),
            auth_mode=auth_mode,
            frontend_dir=Path(os.getenv("SCORESYMPHONY_FRONTEND_DIR", "/app/frontend")),
        )
