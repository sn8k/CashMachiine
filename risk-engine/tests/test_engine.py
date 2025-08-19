# nosec
"""Tests for risk calculations v0.3.1 (2025-08-19)"""
import importlib.util
import sys
from pathlib import Path

__version__ = "0.3.1"

ENGINE_DIR = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


engine = load("risk_engine.engine", ENGINE_DIR / "engine.py")


def test_volatility_target():
    weights = [0.5, 0.5]
    adjusted = engine.volatility_target(weights, 0.1, 0.2)
    assert adjusted == [1.0, 1.0]  # nosec


def test_var_es():
    returns = [-0.1, -0.05, 0.02, -0.2, 0.03]
    var, es = engine.var_es(returns, 0.8)
    assert var > 0  # nosec
    assert es >= var  # nosec


def test_kelly_fraction():
    frac = engine.kelly_fraction(0.1, 0.2, 0.5)
    assert frac == 0.5  # nosec
