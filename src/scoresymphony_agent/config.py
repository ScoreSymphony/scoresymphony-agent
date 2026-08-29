"""Runtime configuration with explicit environment overrides."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    state_dir: Path
    host: str = "0.0.0.0"
    port: int = 8000
    environment: str = "development"

    @classmethod
    def from_env(cls) -> Settings:
        environment = os.getenv("SCORESYMPHONY_ENV", "development")
        if environment not in {"development", "test", "production"}:
            raise ValueError("SCORESYMPHONY_ENV must be development, test, or production")
        return cls(
            state_dir=Path(
                os.getenv("SCORESYMPHONY_STATE_DIR", "/var/lib/scoresymphony-agent")
            ),
            host=os.getenv("SCORESYMPHONY_HOST", "0.0.0.0"),
            port=int(os.getenv("SCORESYMPHONY_PORT", "8000")),
            environment=environment,
        )
