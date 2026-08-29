from __future__ import annotations

from pathlib import Path

from scoresymphony_agent.reviews.base import MockReviewer
from scoresymphony_agent.runtime import AgentRuntime
from scoresymphony_agent.tasks.models import RiskClass, TaskStatus
from scoresymphony_agent.workers.base import MockWorker


def test_mock_end_to_end_loop(tmp_path: Path) -> None:
    runtime = AgentRuntime(tmp_path)
    task = runtime.create_task("Deterministic integration test")
    run, result, review = runtime.execute(task.task_id, MockWorker(), MockReviewer())
    assert result.success is True
    assert run.status.value == "succeeded"
    assert review.review_status.value == "approved"
    assert runtime.tasks.get(task.task_id).status is TaskStatus.COMPLETED
    stored_run = runtime.runs.get(run.run_id)
    assert stored_run.attempts[0].summary
    assert runtime.reviews.get(review.review_id).reviewer_id == "scoresymphony-mock-reviewer"
    assert runtime.events.list()[-1]["payload"]["review_id"] == review.review_id


def test_critical_task_does_not_autorun(tmp_path: Path) -> None:
    runtime = AgentRuntime(tmp_path)
    task = runtime.create_task("Critical task", risk=RiskClass.CRITICAL)
    try:
        runtime.execute(task.task_id, MockWorker(), MockReviewer())
    except PermissionError:
        pass
    else:
        raise AssertionError("Critical task must require a human-controlled path")
