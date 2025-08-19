# nosec
"""Tests for backtester CLI v0.4.0 (2025-08-19)"""
import json
import subprocess  # nosec B404
import sys
from datetime import datetime
from pathlib import Path

from backtester import cli as cli_mod

CLI_PATH = Path(__file__).resolve().parents[1] / "cli.py"


def test_generate_report(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({
        "name": "TestStrategy",
        "symbols": ["AAPL"],
        "initial_capital": 1000,
    }))
    output_path = tmp_path / "report.html"

    class FakeCursor:
        def __init__(self, conn):
            self.conn = conn
            self.data = []

        def execute(self, query, params):
            if query.strip().startswith("SELECT"):
                self.data = [
                    (datetime(2024, 1, 1), 100.0),
                    (datetime(2024, 1, 2), 101.0),
                    (datetime(2024, 1, 3), 102.0),
                ]
            else:
                self.conn.inserted = params

        def fetchall(self):
            return self.data

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeConn:
        def __init__(self):
            self.inserted = None

        def cursor(self):
            return FakeCursor(self)

        def commit(self):
            return None

        def close(self):
            return None

    fake_conn = FakeConn()

    def fake_connect(*args, **kwargs):  # nosec
        return fake_conn

    monkeypatch.setattr(cli_mod.psycopg2, "connect", fake_connect)
    cli_mod.run_backtest(str(config_path), "2024-01-01", "2024-01-03", str(output_path))

    assert output_path.exists()  # nosec
    content = output_path.read_text()
    assert "CAGR" in content  # nosec
    assert "<img" in content  # nosec

    kpis = json.loads(fake_conn.inserted[3])
    assert "CAGR" in kpis  # nosec


def test_install_and_remove(tmp_path):
    subprocess.run([sys.executable, str(CLI_PATH), "--install"], check=True)  # nosec
    reports_dir = Path(__file__).resolve().parents[1] / "reports"
    assert reports_dir.exists()  # nosec
    subprocess.run([sys.executable, str(CLI_PATH), "--remove"], check=True)  # nosec
    assert not reports_dir.exists()  # nosec
