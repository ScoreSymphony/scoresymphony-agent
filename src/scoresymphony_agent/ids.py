"""Identifiers and UTC timestamps shared by runtime components."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def make_id(kind: str) -> str:
    normalized = kind.strip().upper().replace("_", "-")
    if not normalized or not normalized.replace("-", "").isalnum():
        raise ValueError("kind must contain only letters, digits, and hyphens")
    return f"SCORESYMPHONY-{normalized}-{uuid4().hex[:12].upper()}"
