"""File-backed structured review store."""

from __future__ import annotations

from pathlib import Path

from scoresymphony_agent.reviews.models import ReviewResult
from scoresymphony_agent.state.atomic import read_json, write_json_atomic


class ReviewStore:
    def __init__(self, state_dir: Path) -> None:
        self.root = state_dir / "reviews"

    def save(self, review: ReviewResult, *, create_only: bool = True) -> ReviewResult:
        write_json_atomic(self._path(review.review_id), review.to_dict(), create_only=create_only)
        return review

    def get(self, review_id: str) -> ReviewResult:
        path = self._path(review_id)
        if not path.is_file():
            raise KeyError(review_id)
        return ReviewResult.from_dict(read_json(path))

    def list_for_run(self, run_id: str) -> list[ReviewResult]:
        if not self.root.exists():
            return []
        reviews = [ReviewResult.from_dict(read_json(path)) for path in self.root.glob("*.json")]
        return sorted(
            (review for review in reviews if review.run_id == run_id),
            key=lambda review: review.review_round,
        )

    def _path(self, review_id: str) -> Path:
        if not review_id.startswith("SCORESYMPHONY-REVIEW-") or "/" in review_id or "\\" in review_id:
            raise ValueError("Invalid review_id")
        return self.root / f"{review_id}.json"
