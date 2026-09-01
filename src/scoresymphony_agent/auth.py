from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import secrets
from typing import Annotated, Callable

from fastapi import Header, HTTPException, status

from scoresymphony_agent.config import Settings


class Role(StrEnum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    READ_ONLY = "READ_ONLY"


@dataclass(frozen=True, slots=True)
class Principal:
    principal_id: str
    role: Role
    groups: tuple[str, ...] = ()
    email: str | None = None
    display_name: str | None = None


def _groups(raw: str | None) -> tuple[str, ...]:
    if not raw:
        return ()
    return tuple(sorted({part.strip() for part in raw.split(",") if part.strip()}))


def build_principal_resolver(settings: Settings) -> Callable[..., Principal]:
    def resolve(
        remote_user: Annotated[str | None, Header(alias="Remote-User")] = None,
        remote_groups: Annotated[str | None, Header(alias="Remote-Groups")] = None,
        remote_email: Annotated[str | None, Header(alias="Remote-Email")] = None,
        remote_name: Annotated[str | None, Header(alias="Remote-Name")] = None,
        proxy_secret: Annotated[str | None, Header(alias="X-ScoreSymphony-Proxy-Secret")] = None,
    ) -> Principal:
        if settings.auth_mode in {"development", "disabled"}:
            return Principal(principal_id="local-owner", role=Role.OWNER, groups=(settings.owner_group,))

        if settings.auth_mode != "forward_auth":
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="authentication mode is not configured")

        expected = settings.proxy_secret
        if not expected or not proxy_secret or not secrets.compare_digest(expected, proxy_secret):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="untrusted authentication proxy")

        principal_id = (remote_user or "").strip()
        if not principal_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authenticated principal is missing")

        groups = _groups(remote_groups)
        if settings.owner_group in groups:
            role = Role.OWNER
        elif settings.admin_group in groups:
            role = Role.ADMIN
        else:
            role = Role.READ_ONLY

        return Principal(
            principal_id=principal_id,
            role=role,
            groups=groups,
            email=(remote_email or "").strip() or None,
            display_name=(remote_name or "").strip() or None,
        )

    return resolve
