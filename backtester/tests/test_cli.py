# nosec
"""Tests for backtester CLI v0.3.1 (2025-08-19)"""
import json
import subprocess  # nosec B404
import sys
from pathlib import Path

CLI_PATH = Path(__file__).resolve().parents[1] / "cli.py"


def test_generate_report(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"name": "TestStrategy"}))
    output_path = tmp_path / "report.html"
    subprocess.run([
        sys.executable,
        str(CLI_PATH),
        "--config",
        str(config_path),
        "--start-date",
        "2024-01-01",
        "--end-date",
        "2024-06-01",
        "--output",
        str(output_path),
    ], check=True)  # nosec B603
    assert output_path.exists()  # nosec
    content = output_path.read_text()
    assert "Backtest Report" in content  # nosec
    assert "TestStrategy" in content  # nosec


def test_install_and_remove(tmp_path):
    subprocess.run([sys.executable, str(CLI_PATH), "--install"], check=True)  # nosec
    reports_dir = Path(__file__).resolve().parents[1] / "reports"
    assert reports_dir.exists()  # nosec
    subprocess.run([sys.executable, str(CLI_PATH), "--remove"], check=True)  # nosec
    assert not reports_dir.exists()  # nosec
