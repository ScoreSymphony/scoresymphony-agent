from __future__ import annotations

from fastapi import APIRouter

from scoresymphony_agent.services import ControlPlaneService


def build_router(service: ControlPlaneService) -> APIRouter:
    router = APIRouter(prefix="/api/v1")

    @router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "healthy"}

    @router.get("/dashboard")
    def dashboard():
        return service.snapshot()

    @router.get("/proposals")
    def proposals():
        return service.snapshot().proposals

    @router.get("/specifications")
    def specifications():
        return service.snapshot().specifications

    @router.get("/tasks")
    def tasks():
        return service.snapshot().tasks

    @router.get("/runs")
    def runs():
        return service.snapshot().runs

    @router.get("/reviews")
    def reviews():
        return service.snapshot().reviews

    @router.get("/approvals")
    def approvals():
        return service.snapshot().approvals

    @router.get("/system")
    def system():
        return service.system_summary()

    return router
