"""Command-line entry point for the ScoreSymphony Agent bootstrap."""

from __future__ import annotations

import argparse

from scoresymphony_agent import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="scoresymphony-agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show bootstrap application status")
    subparsers.add_parser("version", help="Show application version")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "status":
        print("ScoreSymphony Agent bootstrap: ready")
        return 0

    if args.command == "version":
        print(__version__)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
