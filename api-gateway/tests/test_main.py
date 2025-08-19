"""Unit tests for api-gateway main application v0.2.4 (2025-08-19)"""
from fastapi.testclient import TestClient
from jose import jwt
import importlib.util
from pathlib import Path
import sys

# Ensure project root is on sys.path for common package
sys.path.append(str(Path(__file__).resolve().parents[2]))

MODULE_PATH = Path(__file__).resolve().parents[1] / "main.py"
SPEC = importlib.util.spec_from_file_location("api_gateway_main", MODULE_PATH)
main = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(main)

SECRET_KEY = main.SECRET_KEY
ALGORITHM = main.ALGORITHM

client = TestClient(main.app)


def create_token(role: str):
    return jwt.encode({"role": role}, SECRET_KEY, algorithm=ALGORITHM)


def test_goals_requires_auth():
    response = client.get("/goals")
    assert response.status_code == 403


def test_goals_returns_version_header_and_data():
    token = create_token("user")
    response = client.get("/goals", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.headers["X-API-Version"] == "v0.2.4"
    assert response.json() == {"goals": []}


def test_actions_requires_admin_role():
    token = create_token("user")
    response = client.get("/actions", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    admin_token = create_token("admin")
    response = client.get("/actions", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json() == {"actions": []}


def test_rate_limiting_triggers_after_threshold():
    token = create_token("user")
    from infra.cache import get_redis_client

    client_ip = "testclient"
    redis_client = get_redis_client()
    redis_client.delete(f"rl:{client_ip}")
    for _ in range(main.RATE_LIMIT):
        assert client.get("/goals", headers={"Authorization": f"Bearer {token}"}).status_code == 200
    response = client.get("/goals", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 429
