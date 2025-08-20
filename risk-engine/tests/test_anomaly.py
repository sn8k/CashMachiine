"""Tests for anomaly detection v0.1.0 (2025-08-20)"""
import importlib.util
import sys
from pathlib import Path
import pandas as pd

__version__ = "0.1.0"

ANOM_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ANOM_DIR.parent))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


anomaly = load("risk_engine.anomaly", ANOM_DIR / "anomaly.py")


class DummyConn:
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def cursor(self):
        class Cur:
            def executemany(self, *args, **kwargs):
                pass
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        return Cur()


def test_detect_anomalies_no_data(monkeypatch):
    monkeypatch.setattr(anomaly.psycopg2, "connect", lambda *a, **k: DummyConn())
    monkeypatch.setattr(
        anomaly.pd,
        "read_sql_query",
        lambda *a, **k: pd.DataFrame(
            columns=["date", "portfolio_id", "nav", "ret", "vol", "dd", "var95", "es97"]
        ),
    )
    class DummyProducer:
        def __init__(self, url):
            self.published = []
        def publish(self, event, payload):
            self.published.append((event, payload))
        def close(self):
            pass
    monkeypatch.setattr(anomaly, "EventProducer", DummyProducer)
    anomaly.detect_anomalies()
