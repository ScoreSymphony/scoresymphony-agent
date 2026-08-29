"""Fail-closed semantic validation for structured reviews."""

from __future__ import annotations

from scoresymphony_agent.reviews.models import ReviewResult, ReviewStatus


def validate_review(review: ReviewResult) -> None:
    if review.schema_version != 1:
        raise ValueError("Unsupported review schema_version")
    if review.review_status is ReviewStatus.APPROVED and review.findings:
        raise ValueError("Approved reviews must not contain open findings")
    for finding in review.findings:
        if not finding.component.strip():
            raise ValueError("Finding component must not be empty")
        if not finding.description.strip() or not finding.evidence.strip():
            raise ValueError("Finding description and evidence are required")
        if finding.review_round < 1:
            raise ValueError("review_round must be >= 1")
