from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from scoresymphony_agent.api import build_router
from scoresymphony_agent.config import Settings
from scoresymphony_agent.services import ControlPlaneService
from scoresymphony_agent.state import JsonStateStore


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    store = JsonStateStore(settings.state_root)
    service = ControlPlaneService(settings, store)

    app = FastAPI(
        title="ScoreSymphony Agent",
        version="0.1.0",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )
    app.include_router(build_router(service, settings))

    if settings.frontend_dir.is_dir():
        app.mount("/", StaticFiles(directory=settings.frontend_dir, html=True), name="frontend")
    else:
        @app.get("/")
        def root() -> JSONResponse:
            return JSONResponse({"name": "scoresymphony-agent", "frontend": "not-built", "api_docs": "/api/docs"})

    return app


app = create_app()
