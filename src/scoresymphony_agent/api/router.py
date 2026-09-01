from __future__ import annotations

from fastapi import APIRouter, Depends

from scoresymphony_agent.auth import Principal, build_principal_resolver
from scoresymphony_agent.config import Settings
from scoresymphony_agent.services import ControlPlaneService


def build_router(service: ControlPlaneService, settings: Settings) -> APIRouter:
    router = APIRouter(prefix="/api/v1")
    principal_resolver = build_principal_resolver(settings)

    @router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "healthy"}

    @router.get("/me")
    def me(principal: Principal = Depends(principal_resolver)) -> Principal:
        return principal

    @router.get("/dashboard")
    def dashboard(_: Principal = Depends(principal_resolver)):
        return service.snapshot()

    @router.get("/proposals")
    def proposals(_: Principal = Depends(principal_resolver)):
        return service.snapshot().proposals

    @router.get("/specifications")
    def specifications(_: Principal = Depends(principal_resolver)):
        return service.snapshot().specifications

    @router.get("/tasks")
    def tasks(_: Principal = Depends(principal_resolver)):
        return service.snapshot().tasks

    @router.get("/runs")
    def runs(_: Principal = Depends(principal_resolver)):
        return service.snapshot().runs

    @router.get("/reviews")
    def reviews(_: Principal = Depends(principal_resolver)):
        return service.snapshot().reviews

    @router.get("/approvals")
    def approvals(_: Principal = Depends(principal_resolver)):
        return service.snapshot().approvals

    @router.get("/system")
    def system(_: Principal = Depends(principal_resolver)):
        return service.system_summary()

    return router
