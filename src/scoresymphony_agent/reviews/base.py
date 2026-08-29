"""Reviewer contract independent from Codex or any other provider."""

from __future__ import annotations

from typing import Protocol

from scoresymphony_agent.reviews.models import ReviewResult
from scoresymphony_agent.workers.base import WorkerRequest, WorkerResult


class Reviewer(Protocol):
    reviewer_id: str

    def review(self, request: WorkerRequest, result: WorkerResult) -> ReviewResult: ...


class MockReviewer:
    reviewer_id = "scoresymphony-mock-reviewer"

    def review(self, request: WorkerRequest, result: WorkerResult) -> ReviewResult:
        if not result.success:
            raise ValueError("MockReviewer cannot approve a failed worker result")
        return ReviewResult.approved(
            task_id=request.task_id,
            run_id=request.run_id,
            attempt_id=request.attempt_id,
            reviewer_id=self.reviewer_id,
            recommendation="Mock review approved deterministic test result",
        )
