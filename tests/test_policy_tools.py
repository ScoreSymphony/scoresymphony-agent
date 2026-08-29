from __future__ import annotations

import pytest

from scoresymphony_agent.policies.engine import AccessProfile, PolicyEngine
from scoresymphony_agent.tools.executor import ToolExecutor


def test_tools_are_denied_by_default() -> None:
    policy = PolicyEngine()
    executor = ToolExecutor(policy)
    executor.register("read-name", lambda: "ok", AccessProfile.READ_ONLY)
    with pytest.raises(PermissionError):
        executor.execute("read-name", AccessProfile.DEVELOPMENT)
    assert executor.execute("read-name", AccessProfile.READ_ONLY).output == "ok"
