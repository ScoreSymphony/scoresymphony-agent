"""Command-line entry point for ScoreSymphony Agent."""

from __future__ import annotations

import argparse
import json

import uvicorn

from scoresymphony_agent import __version__
from scoresymphony_agent.config import Settings
from scoresymphony_agent.runtime import AgentRuntime
from scoresymphony_agent.tasks.models import RiskClass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="scoresymphony-agent")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status", help="Show application status")
    subparsers.add_parser("version", help="Show application version")
    subparsers.add_parser("serve", help="Start the HTTP API")

    task = subparsers.add_parser("task", help="Manage tasks")
    task_commands = task.add_subparsers(dest="task_command", required=True)
    create = task_commands.add_parser("create", help="Create a task")
    create.add_argument("title")
    create.add_argument("--description", default="")
    create.add_argument("--risk", choices=[item.value for item in RiskClass], default="low")
    task_commands.add_parser("list", help="List tasks")
    show = task_commands.add_parser("show", help="Show one task")
    show.add_argument("task_id")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    settings = Settings.from_env()

    if args.command == "status":
        print(json.dumps({"service": "scoresymphony-agent", "status": "ready", "environment": settings.environment}))
        return 0
    if args.command == "version":
        print(__version__)
        return 0
    if args.command == "serve":
        uvicorn.run("scoresymphony_agent.api.app:app", host=settings.host, port=settings.port)
        return 0
    if args.command == "task":
        runtime = AgentRuntime(settings.state_dir)
        if args.task_command == "create":
            task = runtime.create_task(args.title, description=args.description, risk=RiskClass(args.risk))
            print(json.dumps(task.to_dict(), indent=2))
            return 0
        if args.task_command == "list":
            print(json.dumps([task.to_dict() for task in runtime.tasks.list()], indent=2))
            return 0
        if args.task_command == "show":
            try:
                print(json.dumps(runtime.tasks.get(args.task_id).to_dict(), indent=2))
                return 0
            except (KeyError, ValueError):
                print("Task not found")
                return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
