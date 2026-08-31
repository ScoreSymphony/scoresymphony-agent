from __future__ import annotations

from scoresymphony_agent.config import Settings
from scoresymphony_agent.domain import PlatformSnapshot, SystemSummary
from scoresymphony_agent.state import StateStore


class ControlPlaneService:
    def __init__(self, settings: Settings, store: StateStore) -> None:
        self.settings = settings
        self.store = store

    def snapshot(self) -> PlatformSnapshot:
        return self.store.load()

    def system_summary(self) -> SystemSummary:
        return SystemSummary(
            environment=self.settings.environment,
            state_backend=self.store.__class__.__name__,
            capabilities={
                "human_control_ui": "IMPLEMENTED_BOOTSTRAP",
                "shared_state": "IMPLEMENTED_BOOTSTRAP",
                "worker_adapters": "PREPARED",
                "fcc_implementation": "PLANNED",
                "codex_review": "PLANNED",
                "gpu_worker": "PLANNED",
                "resource_scheduler": "PLANNED",
                "worktree_manager": "PLANNED",
            },
        )
