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

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Finding:
        return cls(
            finding_id=str(value["finding_id"]),
            severity=Severity(value["severity"]),
            component=str(value["component"]),
            description=str(value["description"]),
            evidence=str(value["evidence"]),
            recommendation=str(value.get("recommendation", "")),
            review_round=int(value["review_round"]),
        )


@dataclass(slots=True)
class ReviewResult:
    review_id: str
    task_id: str
    run_id: str
    attempt_id: str
    reviewer_id: str
    review_round: int
    review_status: ReviewStatus
    findings: list[Finding] = field(default_factory=list)
    scope_assessment: str = ""
    test_assessment: str = ""
    unauthorized_changes: list[str] = field(default_factory=list)
    recommendation: str = ""
    created_at: str = field(default_factory=utc_now)
    schema_version: int = 1

    @classmethod
    def approved(
        cls,
        *,
        task_id: str,
        run_id: str,
        attempt_id: str,
        reviewer_id: str,
        review_round: int = 1,
        recommendation: str = "",
    ) -> ReviewResult:
        return cls(
            review_id=make_id("REVIEW"),
            task_id=task_id,
            run_id=run_id,
            attempt_id=attempt_id,
            reviewer_id=reviewer_id,
            review_round=review_round,
            review_status=ReviewStatus.APPROVED,
            recommendation=recommendation,
        )

    @classmethod
    def blocked(
        cls,
        *,
        task_id: str,
        run_id: str,
        attempt_id: str,
        reviewer_id: str,
        recommendation: str,
        review_round: int = 1,
    ) -> ReviewResult:
        return cls(
            review_id=make_id("REVIEW"),
            task_id=task_id,
            run_id=run_id,
            attempt_id=attempt_id,
            reviewer_id=reviewer_id,
            review_round=review_round,
            review_status=ReviewStatus.BLOCKED,
            recommendation=recommendation,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ReviewResult:
        return cls(
            review_id=str(value["review_id"]),
            task_id=str(value["task_id"]),
            run_id=str(value["run_id"]),
            attempt_id=str(value["attempt_id"]),
            reviewer_id=str(value["reviewer_id"]),
            review_round=int(value["review_round"]),
            review_status=ReviewStatus(value["review_status"]),
            findings=[Finding.from_dict(item) for item in value.get("findings", [])],
            scope_assessment=str(value.get("scope_assessment", "")),
            test_assessment=str(value.get("test_assessment", "")),
            unauthorized_changes=list(value.get("unauthorized_changes", [])),
            recommendation=str(value.get("recommendation", "")),
            created_at=str(value["created_at"]),
            schema_version=int(value.get("schema_version", 1)),
        )
