from __future__ import annotations

from pathlib import Path

import pytest

from scoresymphony_agent.reviews.models import Finding, ReviewResult, Severity
from scoresymphony_agent.reviews.store import ReviewStore
from scoresymphony_agent.reviews.validator import validate_review


def approved_review() -> ReviewResult:
    return ReviewResult.approved(
        task_id="SCORESYMPHONY-TASK-000000000001",
        run_id="SCORESYMPHONY-RUN-000000000001",
        attempt_id="SCORESYMPHONY-ATTEMPT-000000000001",
        reviewer_id="test-reviewer",
    )


def test_approved_review_without_findings_is_valid() -> None:
    validate_review(approved_review())


def test_approved_review_with_findings_fails_closed() -> None:
    review = approved_review()
    review.findings.append(
        Finding.new(
            severity=Severity.MAJOR,
            component="x.py",
            description="Problem",
            evidence="Evidence",
            recommendation="Fix",
            review_round=1,
        )
    )
    with pytest.raises(ValueError):
        validate_review(review)


def test_review_store_roundtrip(tmp_path: Path) -> None:
    store = ReviewStore(tmp_path)
    review = approved_review()
    store.save(review)
    loaded = store.get(review.review_id)
    assert loaded.review_id == review.review_id
    assert store.list_for_run(review.run_id)[0].reviewer_id == "test-reviewer"
