# nosec
"""Tests for stress scenarios v0.1.0 (2025-08-19)"""
import importlib.util
import sys
from pathlib import Path

__version__ = "0.1.0"

ENGINE_DIR = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


stress = load("risk_engine.stress_tests", ENGINE_DIR / "stress_tests.py")


def test_historical_scenario():
    prices = [100.0, 95.0, 90.0]
    result = stress.historical_scenario(prices)
    assert len(result) == len(prices)  # nosec
    assert result[-1] <= prices[-1]  # nosec


def test_hypothetical_scenario():
    prices = [100.0, 100.0]
    shocks = [-0.1, -0.2]
    result = stress.hypothetical_scenario(prices, shocks)
    assert result == [90.0, 80.0]  # nosec
