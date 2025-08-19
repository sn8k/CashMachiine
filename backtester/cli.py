#!/usr/bin/env python3
"""backtester CLI v0.3.1 (2025-08-19)"""
import argparse
import json
import os
import subprocess  # nosec B404
import shutil
from datetime import datetime

REPORT_DIR = os.path.join(os.path.dirname(__file__), "reports")


def install_service():
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    subprocess.run([script_path], check=True)  # nosec B603
    os.makedirs(REPORT_DIR, exist_ok=True)


def remove_service():
    script_path = os.path.join(os.path.dirname(__file__), "remove.sh")
    subprocess.run([script_path], check=True)  # nosec B603
    shutil.rmtree(REPORT_DIR, ignore_errors=True)


def run_backtest(config_path: str, start_date: str, end_date: str, output_path: str | None) -> None:
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    os.makedirs(REPORT_DIR, exist_ok=True)
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(REPORT_DIR, f"report_{timestamp}.html")

    html = (
        "<html><body><h1>Backtest Report</h1>"
        f"<p>Strategy: {config.get('name', 'unknown')}</p>"
        f"<p>Start: {start_date}</p>"
        f"<p>End: {end_date}</p>"
        "</body></html>"
    )

    with open(output_path, "w", encoding="utf-8") as out:
        out.write(html)
    print(f"Report generated at {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Backtester controller v0.3.1")
    parser.add_argument("--install", action="store_true", help="Install backtester service")
    parser.add_argument("--remove", action="store_true", help="Remove backtester service")
    parser.add_argument("--config", help="Path to strategy config JSON")
    parser.add_argument("--start-date", help="Backtest start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Backtest end date (YYYY-MM-DD)")
    parser.add_argument("--output", help="Output HTML report path")
    args = parser.parse_args()

    if args.install:
        install_service()
        return
    if args.remove:
        remove_service()
        return

    if not (args.config and args.start_date and args.end_date):
        parser.error("--config, --start-date and --end-date are required unless using --install or --remove")

    run_backtest(args.config, args.start_date, args.end_date, args.output)


if __name__ == "__main__":
    main()
