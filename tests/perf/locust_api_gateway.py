"""Locust load test for api-gateway v0.1.0 (2025-08-20)"""
from locust import HttpUser, task, between, events
import os

THRESHOLD_MS = float(os.getenv("API_GATEWAY_THRESHOLD_MS", "500"))

class ApiGatewayUser(HttpUser):
    wait_time = between(1, 2)
    host = os.getenv("API_GATEWAY_URL", "http://localhost:8000")

    @task
    def docs(self):
        self.client.get("/docs")

@events.quitting.add_listener
def _(environment, **kw):
    avg = environment.stats.total.avg_response_time
    if avg > THRESHOLD_MS:
        print(f"Average response time {avg:.2f} ms exceeded threshold {THRESHOLD_MS} ms")
        environment.process_exit_code = 1
