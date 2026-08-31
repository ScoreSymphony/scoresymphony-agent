from pathlib import Path

from fastapi.testclient import TestClient

from scoresymphony_agent.app import create_app
from scoresymphony_agent.config import Settings


def make_client(tmp_path: Path) -> TestClient:
    settings = Settings(environment="test", state_root=tmp_path / "state", auth_mode="disabled", frontend_dir=tmp_path / "missing-frontend")
    return TestClient(create_app(settings))


def test_health(tmp_path: Path) -> None:
    response = make_client(tmp_path).get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_control_plane_surfaces_exist(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    for path in ("/api/v1/proposals", "/api/v1/specifications", "/api/v1/tasks", "/api/v1/runs", "/api/v1/reviews", "/api/v1/approvals"):
        response = client.get(path)
        assert response.status_code == 200
        assert response.json() == []


def test_system_reports_bootstrap_capabilities(tmp_path: Path) -> None:
    response = make_client(tmp_path).get("/api/v1/system")
    assert response.status_code == 200
    body = response.json()
    assert body["environment"] == "test"
    assert body["capabilities"]["codex_review"] == "PLANNED"


def test_forward_auth_rejects_untrusted_headers(tmp_path: Path) -> None:
    settings = Settings(
        environment="test",
        state_root=tmp_path / "state",
        auth_mode="forward_auth",
        frontend_dir=tmp_path / "missing-frontend",
        proxy_secret="trusted-secret",
    )
    client = TestClient(create_app(settings))

    response = client.get(
        "/api/v1/me",
        headers={"Remote-User": "alice", "Remote-Groups": "scoresymphony-owner"},
    )
    assert response.status_code == 401


def test_forward_auth_maps_authenticated_principal_role(tmp_path: Path) -> None:
    settings = Settings(
        environment="test",
        state_root=tmp_path / "state",
        auth_mode="forward_auth",
        frontend_dir=tmp_path / "missing-frontend",
        proxy_secret="trusted-secret",
    )
    client = TestClient(create_app(settings))

    response = client.get(
        "/api/v1/me",
        headers={
            "X-ScoreSymphony-Proxy-Secret": "trusted-secret",
            "Remote-User": "alice",
            "Remote-Groups": "developers,scoresymphony-owner",
            "Remote-Email": "alice@example.test",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["principal_id"] == "alice"
    assert body["role"] == "OWNER"
    assert body["email"] == "alice@example.test"
