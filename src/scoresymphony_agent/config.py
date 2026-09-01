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
    proxy_secret: str | None = None
    owner_group: str = "scoresymphony-owner"
    admin_group: str = "scoresymphony-admin"

    @classmethod
    def from_env(cls) -> "Settings":
        environment = os.getenv("SCORESYMPHONY_ENV", "development")
        default_state = "/var/lib/scoresymphony-agent" if environment == "production" else "./state-local"
        auth_mode = os.getenv("SCORESYMPHONY_AUTH_MODE", "development")
        proxy_secret = os.getenv("SCORESYMPHONY_PROXY_SECRET")

        if auth_mode not in {"development", "disabled", "forward_auth"}:
            raise RuntimeError(f"unsupported authentication mode: {auth_mode}")
        if environment == "production" and auth_mode != "forward_auth":
            raise RuntimeError("production requires SCORESYMPHONY_AUTH_MODE=forward_auth")
        if environment == "production" and not proxy_secret:
            raise RuntimeError("production forward authentication requires SCORESYMPHONY_PROXY_SECRET")

        return cls(
            environment=environment,
            state_root=Path(os.getenv("SCORESYMPHONY_STATE_ROOT", default_state)),
            auth_mode=auth_mode,
            frontend_dir=Path(os.getenv("SCORESYMPHONY_FRONTEND_DIR", "/app/frontend")),
            proxy_secret=proxy_secret,
            owner_group=os.getenv("SCORESYMPHONY_OWNER_GROUP", "scoresymphony-owner"),
            admin_group=os.getenv("SCORESYMPHONY_ADMIN_GROUP", "scoresymphony-admin"),
        )
