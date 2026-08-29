"""Small deny-by-default authorization policy for tools."""

from __future__ import annotations

from enum import StrEnum


class AccessProfile(StrEnum):
    READ_ONLY = "read_only"
    DEVELOPMENT = "development"
    ELEVATED = "elevated"
    ADMIN = "admin"


class PolicyEngine:
    def __init__(self) -> None:
        self._tool_profiles: dict[str, set[AccessProfile]] = {}

    def allow_tool(self, tool_name: str, *profiles: AccessProfile) -> None:
        if not tool_name.strip() or not profiles:
            raise ValueError("tool_name and at least one profile are required")
        self._tool_profiles[tool_name] = set(profiles)

    def authorize_tool(self, tool_name: str, profile: AccessProfile) -> bool:
        return profile in self._tool_profiles.get(tool_name, set())

    def require_tool(self, tool_name: str, profile: AccessProfile) -> None:
        if not self.authorize_tool(tool_name, profile):
            raise PermissionError(f"Tool {tool_name!r} is not allowed for {profile.value}")
