"""Locust performance test for strategy-engine computations v0.1.0 (2025-08-20)"""
from locust import User, task, between, events
import time
import os
from strategies.core import CoreStrategy

THRESHOLD_MS = float(os.getenv("STRATEGY_ENGINE_THRESHOLD_MS", "100"))

class StrategyEngineUser(User):
    wait_time = between(1, 2)

    @task
    def compute(self):
        start = time.time()
        strategy = CoreStrategy()
        signals = strategy.signals([])
        strategy.target_weights(signals)
        total_time = (time.time() - start) * 1000
        events.request_success.fire(
            request_type="compute",
            name="core_strategy",
            response_time=total_time,
            response_length=0,
        )

@events.quitting.add_listener
def _(environment, **kw):
    avg = environment.stats.total.avg_response_time
    if avg > THRESHOLD_MS:
        print(f"Average compute time {avg:.2f} ms exceeded threshold {THRESHOLD_MS} ms")
        environment.process_exit_code = 1
