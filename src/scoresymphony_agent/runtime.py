"""Application service coordinating persisted state without binding to a model provider."""

from __future__ import annotations

from scoresymphony_agent.events.store import EventStore
from scoresymphony_agent.ids import utc_now
from scoresymphony_agent.reviews.base import Reviewer
from scoresymphony_agent.reviews.models import ReviewResult, ReviewStatus
from scoresymphony_agent.reviews.validator import validate_review
from scoresymphony_agent.runs.models import Attempt, Run, RunStatus
from scoresymphony_agent.runs.store import RunStore
from scoresymphony_agent.tasks.models import RiskClass, Task, TaskStatus
from scoresymphony_agent.tasks.store import TaskStore
from scoresymphony_agent.workers.base import Worker, WorkerRequest, WorkerResult


class AgentRuntime:
    def __init__(self, state_dir) -> None:
        self.tasks = TaskStore(state_dir)
        self.runs = RunStore(state_dir)
        self.events = EventStore(state_dir)

    def create_task(
        self,
        title: str,
        *,
        description: str = "",
        risk: RiskClass = RiskClass.LOW,
        scope: list[str] | None = None,
        acceptance_criteria: list[str] | None = None,
    ) -> Task:
        task = Task.new(
            title,
            description=description,
            risk=risk,
            scope=scope,
            acceptance_criteria=acceptance_criteria,
        )
        self.tasks.create(task)
        self.events.append(
            event_type="task.created",
            component="runtime",
            result="ok",
            task_id=task.task_id,
        )
        return task

    def execute(self, task_id: str, worker: Worker, reviewer: Reviewer) -> tuple[Run, WorkerResult, ReviewResult]:
        task = self.tasks.get(task_id)
        if task.risk is RiskClass.CRITICAL:
            raise PermissionError("Critical tasks require a human-controlled execution path")
        if task.status not in {TaskStatus.PENDING, TaskStatus.BLOCKED}:
            raise ValueError(f"Task cannot run from status {task.status.value}")

        run = Run.new(task.task_id)
        attempt = Attempt.new(worker.agent_id)
        attempt.status = RunStatus.RUNNING
        attempt.started_at = utc_now()
        run.attempts.append(attempt)
        run.status = RunStatus.RUNNING
        run.updated_at = utc_now()
        self.runs.save(run, create_only=True)
        task.status = TaskStatus.RUNNING
        task.updated_at = utc_now()
        self.tasks.save(task)
        self.events.append(event_type="run.started", component="runtime", result="ok", task_id=task.task_id, run_id=run.run_id, attempt_id=attempt.attempt_id)

        request = WorkerRequest(
            task_id=task.task_id,
            run_id=run.run_id,
            attempt_id=attempt.attempt_id,
            title=task.title,
            description=task.description,
            scope=task.scope,
            acceptance_criteria=task.acceptance_criteria,
        )
        worker_result = worker.run(request)
        attempt.ended_at = utc_now()
        attempt.exit_code = worker_result.exit_code
        attempt.status = RunStatus.SUCCEEDED if worker_result.success else RunStatus.FAILED

        if not worker_result.success:
            run.status = RunStatus.FAILED
            task.status = TaskStatus.BLOCKED
            attempt.failure_reason = worker_result.summary
            review = ReviewResult(
                review_id="SCORESYMPHONY-REVIEW-NOT-RUN",
                review_status=ReviewStatus.BLOCKED,
                recommendation="Worker failed before review",
            )
        else:
            review = reviewer.review(request, worker_result)
            validate_review(review)
            if review.review_status is ReviewStatus.APPROVED:
                run.status = RunStatus.SUCCEEDED
                task.status = TaskStatus.COMPLETED
            else:
                run.status = RunStatus.BLOCKED
                task.status = TaskStatus.BLOCKED

        run.updated_at = utc_now()
        task.updated_at = utc_now()
        self.runs.save(run)
        self.tasks.save(task)
        self.events.append(event_type="run.finished", component="runtime", result=run.status.value, task_id=task.task_id, run_id=run.run_id, attempt_id=attempt.attempt_id, payload={"review_status": review.review_status.value})
        return run, worker_result, review
