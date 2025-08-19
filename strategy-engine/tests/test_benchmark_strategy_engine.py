"""Benchmark tests for strategy-engine v0.1.0 (2025-08-19)"""
import importlib.util
import sys
from pathlib import Path

from pytest_benchmark.fixture import BenchmarkFixture

ENGINE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ENGINE_DIR.parent))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


interface = load("strategy_engine.interface", ENGINE_DIR / "interface.py")
core = load("strategy_engine.strategies.core", ENGINE_DIR / "strategies/core.py")


def test_core_strategy_signals_benchmark(benchmark: BenchmarkFixture):
    strategy = core.CoreStrategy()
    benchmark(strategy.signals, {})
