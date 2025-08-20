# nosec
"""Unit tests for api-gateway main application v0.2.9 (2025-08-20)"""
import os

os.environ["OTEL_SDK_DISABLED"] = "true"

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
    return jwt.encode({"role": role, "tenant_id": 1}, SECRET_KEY, algorithm=ALGORITHM)


def test_goals_requires_auth():
    response = client.get("/goals")
    assert response.status_code == 403  # nosec


def test_goals_returns_version_header_and_data():
    token = create_token("user")
    response = client.get("/goals", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  # nosec
    assert response.headers["X-API-Version"] == "v0.2.9"  # nosec
    assert response.json() == {"goals": []}  # nosec


def test_actions_requires_admin_role():
    token = create_token("user")
    response = client.get("/actions", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403  # nosec

    admin_token = create_token("admin")
    response = client.get("/actions", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200  # nosec
    assert response.json() == {"actions": []}  # nosec


def test_post_goal_requires_admin_role():
    token = create_token("user")
    response = client.post("/goals", json={}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403  # nosec

    admin_token = create_token("admin")
    response = client.post("/goals", json={"user_id": 1, "name": "x"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200  # nosec
    assert response.json() == {"goal": {}}  # nosec


def test_goal_status_endpoint():
    token = create_token("user")
    response = client.get("/goals/1/status", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  # nosec
    assert response.json() == {"goal_id": 1, "done": 0, "pending": 0}  # nosec


def test_actions_today_and_check():
    token = create_token("user")
    response = client.get("/actions/today", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  # nosec
    assert response.json() == {"actions": []}  # nosec

    user_response = client.post("/actions/1/check", headers={"Authorization": f"Bearer {token}"})
    assert user_response.status_code == 403  # nosec

    admin_token = create_token("admin")
    admin_response = client.post("/actions/1/check", headers={"Authorization": f"Bearer {admin_token}"})
    assert admin_response.status_code == 404  # nosec


def test_orders_preview_endpoint():
    token = create_token("user")
    response = client.get("/orders/preview", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  # nosec
    assert response.json() == {"orders": []}  # nosec


def test_rate_limiting_triggers_after_threshold():
    token = create_token("user")
    from infra.cache import get_redis_client

    client_ip = "testclient"
    redis_client = get_redis_client()
    redis_client.delete(f"rl:{client_ip}")
    for _ in range(main.RATE_LIMIT):
        assert client.get("/goals", headers={"Authorization": f"Bearer {token}"}).status_code == 200  # nosec
    response = client.get("/goals", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 429  # nosec


def test_analytics_requires_admin_role():
    from infra.cache import get_redis_client

    redis_client = get_redis_client()
    redis_client.delete("rl:testclient")

    token = create_token("user")
    response = client.get("/analytics", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403  # nosec

    admin_token = create_token("admin")
    response = client.get("/analytics", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200  # nosec
    body = response.json()
    assert "db_metrics" in body and "observability" in body  # nosec
