from __future__ import annotations

import unittest

from scoresymphony_agent.app import build_parser


class AppBootstrapTests(unittest.TestCase):
    def test_status_command_parses(self) -> None:
        args = build_parser().parse_args(["status"])
        self.assertEqual(args.command, "status")

    def test_version_command_parses(self) -> None:
        args = build_parser().parse_args(["version"])
        self.assertEqual(args.command, "version")


if __name__ == "__main__":
    unittest.main()
