from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from pydantic import BaseModel, Field


class EntitySummary(BaseModel):
    id: str
    title: str
    status: str
    updated_at: datetime
    meta: dict[str, Any] = Field(default_factory=dict)


class SystemSummary(BaseModel):
    environment: str
    state_backend: str
    status: Literal["healthy", "degraded", "blocked"] = "healthy"
    workers: list[dict[str, Any]] = Field(default_factory=list)
    capabilities: dict[str, str] = Field(default_factory=dict)


class PlatformSnapshot(BaseModel):
    schema_version: int = 1
    state_revision: int = 0
    last_event_sequence: int = 0
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    proposals: list[EntitySummary] = Field(default_factory=list)
    specifications: list[EntitySummary] = Field(default_factory=list)
    tasks: list[EntitySummary] = Field(default_factory=list)
    runs: list[EntitySummary] = Field(default_factory=list)
    reviews: list[EntitySummary] = Field(default_factory=list)
    approvals: list[EntitySummary] = Field(default_factory=list)
