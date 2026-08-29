"""Deterministic tool registry; arbitrary shell execution is intentionally absent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from scoresymphony_agent.policies.engine import AccessProfile, PolicyEngine


@dataclass(frozen=True, slots=True)
class ToolResult:
    tool: str
    success: bool
    output: Any


ToolCallable = Callable[..., Any]


class ToolExecutor:
    def __init__(self, policy: PolicyEngine) -> None:
        self._policy = policy
        self._tools: dict[str, ToolCallable] = {}

    def register(self, name: str, function: ToolCallable, *profiles: AccessProfile) -> None:
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")
        self._tools[name] = function
        self._policy.allow_tool(name, *profiles)

    def execute(self, name: str, profile: AccessProfile, **kwargs: Any) -> ToolResult:
        self._policy.require_tool(name, profile)
        function = self._tools.get(name)
        if function is None:
            raise LookupError(name)
        return ToolResult(tool=name, success=True, output=function(**kwargs))
