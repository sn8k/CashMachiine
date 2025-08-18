"""Unit test stubs for strategy interface v0.1.0 (2025-08-18)"""
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


interface = load("strategy_engine.interface", ENGINE_DIR / "interface.py")
core = load("strategy_engine.strategies.core", ENGINE_DIR / "strategies/core.py")
satellite = load("strategy_engine.strategies.satellite", ENGINE_DIR / "strategies/satellite.py")


def test_core_strategy_interface():
    strategy = core.CoreStrategy()
    sigs = strategy.signals({})
    weights = strategy.target_weights(sigs)
    assert isinstance(sigs, dict)
    assert isinstance(weights, dict)


def test_satellite_strategy_interface():
    strategy = satellite.SatelliteStrategy()
    sigs = strategy.signals({})
    weights = strategy.target_weights(sigs)
    assert isinstance(sigs, dict)
    assert isinstance(weights, dict)
