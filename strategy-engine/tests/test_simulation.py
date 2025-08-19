# nosec
"""Unit tests for simulation utilities v0.1.0 (2025-08-20)"""
import importlib.util
import sys
from pathlib import Path
import types

__version__ = "0.1.1"

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
sim = load("strategy_engine.simulation", ENGINE_DIR / "simulation.py")


def test_probability_of_hitting():
    paths = sim.generate_paths(100, 0.05, 0.2, 5, 100, seed=1)
    prob = sim.probability_of_hitting(paths, 110)
    assert 0.0 <= prob <= 1.0  # nosec
