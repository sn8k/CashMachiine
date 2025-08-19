# nosec
"""Unit test stubs for strategy interface v0.1.2 (2025-08-20)"""
import importlib.util
import sys
from pathlib import Path
import types

__version__ = "0.1.2"

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
interface = load("strategy_engine.interface", ENGINE_DIR / "interface.py")
core = load("strategy_engine.strategies.core", ENGINE_DIR / "strategies/core.py")
satellite = load("strategy_engine.strategies.satellite", ENGINE_DIR / "strategies/satellite.py")


def test_core_strategy_interface(monkeypatch):
    monkeypatch.setattr(
        core, "adjust_risk", lambda **_: {"weights": [1.0], "explanation": "stub"}
    )
    strategy = core.CoreStrategy()
    sigs = strategy.signals({"SPY": {"close": 101, "prev_close": 100}})
    weights = strategy.target_weights(sigs)
    assert isinstance(sigs, dict)  # nosec
    assert isinstance(weights, dict)  # nosec
    assert isinstance(strategy.explain(), str)  # nosec


def test_satellite_strategy_interface(monkeypatch):
    monkeypatch.setattr(
        satellite, "adjust_risk", lambda **_: {"weights": [0.1], "explanation": "stub"}
    )
    strategy = satellite.SatelliteStrategy()
    sigs = strategy.signals({"BTC": {"close": 101, "prev_close": 100}})
    weights = strategy.target_weights(sigs)
    assert isinstance(sigs, dict)  # nosec
    assert isinstance(weights, dict)  # nosec
    assert isinstance(strategy.explain(), str)  # nosec
