from __future__ import annotations

from typing import Any, Protocol


class WorkerAdapter(Protocol):
    async def run(self, task_id: str, context: dict[str, Any]) -> dict[str, Any]: ...
    async def status(self, run_id: str) -> dict[str, Any]: ...
    async def cancel(self, run_id: str) -> None: ...


class ReviewAdapter(Protocol):
    async def review(self, run_id: str, evidence: dict[str, Any]) -> dict[str, Any]: ...


class SystemMetricsAdapter(Protocol):
    async def snapshot(self) -> dict[str, Any]: ...
