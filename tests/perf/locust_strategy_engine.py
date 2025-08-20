"""Locust performance test for strategy-engine computations v0.1.3 (2025-08-20)"""
from locust import User, task, between, events
import time
import os
import importlib.util
import sys
from pathlib import Path
import types

ENGINE_DIR = Path(__file__).resolve().parents[2] / "strategy-engine"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


pkg = types.ModuleType("strategy_engine")
pkg.__path__ = [str(ENGINE_DIR)]
sys.modules["strategy_engine"] = pkg
load("strategy_engine.interface", ENGINE_DIR / "interface.py")
core = load("strategy_engine.strategies.core", ENGINE_DIR / "strategies/core.py")
CoreStrategy = core.CoreStrategy

THRESHOLD_MS = float(os.getenv("STRATEGY_ENGINE_THRESHOLD_MS", "100"))


class StrategyEngineUser(User):
    wait_time = between(1, 2)

    @task
    def compute(self):
        start = time.time()
        strategy = CoreStrategy()
        signals = strategy.signals({})
        strategy.target_weights(signals)
        total_time = (time.time() - start) * 1000
        self.environment.events.request.fire(
            request_type="compute",
            name="core_strategy",
            response_time=total_time,
            response_length=0,
            exception=None,
        )


@events.quitting.add_listener
def _(environment, **kw):
    avg = environment.stats.total.avg_response_time
    if avg > THRESHOLD_MS:
        print(f"Average compute time {avg:.2f} ms exceeded threshold {THRESHOLD_MS} ms")
        environment.process_exit_code = 1
