# nosec
"""Tests for ML forecast utilities v0.1.0 (2025-08-19)"""
import importlib.util
import sys
from pathlib import Path
import types

__version__ = "0.1.0"

ENGINE_DIR = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


pkg = types.ModuleType("strategy_engine")
pkg.__path__ = [str(ENGINE_DIR)]
sys.modules["strategy_engine"] = pkg
ml = load("strategy_engine.ml_forecast", ENGINE_DIR / "ml_forecast.py")


def test_forecast_prices_returns_float(tmp_path):
    pred = ml.forecast_prices("TEST", [1, 2, 3])
    assert isinstance(pred, float)  # nosec
