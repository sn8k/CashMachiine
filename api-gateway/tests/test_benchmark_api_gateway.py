# nosec
"""Benchmark tests for api-gateway v0.3.0 (2025-08-20)"""
import os

os.environ["OTEL_SDK_DISABLED"] = "true"

from fastapi.testclient import TestClient
from jose import jwt
import importlib.util
from pathlib import Path
import sys

from pytest_benchmark.fixture import BenchmarkFixture

# Ensure project root on sys.path for common package
sys.path.append(str(Path(__file__).resolve().parents[2]))

MODULE_PATH = Path(__file__).resolve().parents[1] / "main.py"
SPEC = importlib.util.spec_from_file_location("api_gateway_main", MODULE_PATH)
main = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(main)

client = TestClient(main.app)
SECRET_KEY = main.SECRET_KEY
ALGORITHM = main.ALGORITHM


def create_token(role: str):
    return jwt.encode({"role": role, "tenant_id": 1}, SECRET_KEY, algorithm=ALGORITHM)


def bench_request():
    token = create_token("user")
    client.get("/goals", headers={"Authorization": f"Bearer {token}"})


def test_get_goals_benchmark(benchmark: BenchmarkFixture):
    benchmark(bench_request)
