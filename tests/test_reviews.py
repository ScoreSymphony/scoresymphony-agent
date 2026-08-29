from __future__ import annotations

import pytest

from scoresymphony_agent.reviews.models import Finding, ReviewResult, ReviewStatus, Severity
from scoresymphony_agent.reviews.validator import validate_review


def test_approved_review_without_findings_is_valid() -> None:
    validate_review(ReviewResult.approved())


def test_approved_review_with_findings_fails_closed() -> None:
    review = ReviewResult(
        review_id="SCORESYMPHONY-REVIEW-TEST",
        review_status=ReviewStatus.APPROVED,
        findings=[Finding.new(severity=Severity.MAJOR, component="x.py", description="Problem", evidence="Evidence", recommendation="Fix", review_round=1)],
    )
    with pytest.raises(ValueError):
        validate_review(review)
