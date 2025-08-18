"""Tests for backtester CLI v0.3.0 (2025-08-18)"""
import json
import subprocess
from pathlib import Path

CLI_PATH = Path(__file__).resolve().parents[1] / "cli.py"


def test_generate_report(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"name": "TestStrategy"}))
    output_path = tmp_path / "report.html"
    subprocess.run([
        "python",
        str(CLI_PATH),
        "--config",
        str(config_path),
        "--start-date",
        "2024-01-01",
        "--end-date",
        "2024-06-01",
        "--output",
        str(output_path),
    ], check=True)
    assert output_path.exists()
    content = output_path.read_text()
    assert "Backtest Report" in content
    assert "TestStrategy" in content


def test_install_and_remove(tmp_path):
    subprocess.run(["python", str(CLI_PATH), "--install"], check=True)
    reports_dir = Path(__file__).resolve().parents[1] / "reports"
    assert reports_dir.exists()
    subprocess.run(["python", str(CLI_PATH), "--remove"], check=True)
    assert not reports_dir.exists()
