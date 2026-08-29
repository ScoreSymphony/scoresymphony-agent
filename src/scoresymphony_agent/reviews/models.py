"""Provider-neutral structured review contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from scoresymphony_agent.ids import make_id, utc_now


class ReviewStatus(StrEnum):
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    BLOCKED = "blocked"


class Severity(StrEnum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


@dataclass(slots=True)
class Finding:
    finding_id: str
    severity: Severity
    component: str
    description: str
    evidence: str
    recommendation: str
    review_round: int

    @classmethod
    def new(cls, **kwargs: Any) -> Finding:
        return cls(finding_id=make_id("FINDING"), **kwargs)


@dataclass(slots=True)
class ReviewResult:
    review_id: str
    review_status: ReviewStatus
    findings: list[Finding] = field(default_factory=list)
    scope_assessment: str = ""
    test_assessment: str = ""
    unauthorized_changes: list[str] = field(default_factory=list)
    recommendation: str = ""
    created_at: str = field(default_factory=utc_now)
    schema_version: int = 1

    @classmethod
    def approved(cls, recommendation: str = "") -> ReviewResult:
        return cls(
            review_id=make_id("REVIEW"),
            review_status=ReviewStatus.APPROVED,
            recommendation=recommendation,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
