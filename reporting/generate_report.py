#!/usr/bin/env python3
# generate_report.py v0.1.0 (2025-08-20)
"""Generate PDF reports for actions, orders, KYC and metrics."""

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

try:
    from weasyprint import HTML
except ImportError:  # pragma: no cover
    HTML = None

REPORT_DIR = Path('reports')
REPORT_FILE = REPORT_DIR / 'daily_report.pdf'


def install_dependencies() -> None:
    """Install required Python packages."""
    subprocess.run(["python", "-m", "pip", "install", "weasyprint"], check=False)


def remove_reports() -> None:
    """Remove generated reports and optional dependency."""
    if REPORT_DIR.exists():
        shutil.rmtree(REPORT_DIR)
    subprocess.run(["python", "-m", "pip", "uninstall", "-y", "weasyprint"], check=False)


def generate_report() -> None:
    """Generate a simple PDF report with placeholder data."""
    REPORT_DIR.mkdir(exist_ok=True)
    data = {
        "actions": ["Review portfolio", "Rebalance assets"],
        "orders": ["BUY AAPL 10", "SELL GOOGL 5"],
        "kyc": ["Alice: verified", "Bob: pending"],
        "metrics": {"total_orders": 2, "verified_users": 1},
    }
    html_parts = ["<h1>Daily Report</h1>"]
    for section, items in data.items():
        html_parts.append(f"<h2>{section.title()}</h2>")
        if isinstance(items, dict):
            html_parts.append("<ul>")
            for key, value in items.items():
                html_parts.append(f"<li>{key}: {value}</li>")
            html_parts.append("</ul>")
        else:
            html_parts.append("<ul>")
            for item in items:
                html_parts.append(f"<li>{item}</li>")
            html_parts.append("</ul>")
    html_content = "".join(html_parts)
    if HTML is None:
        raise SystemExit("WeasyPrint is not installed. Run with --install first.")
    HTML(string=html_content).write_pdf(str(REPORT_FILE))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PDF reports.")
    parser.add_argument("--install", action="store_true", help="install dependencies")
    parser.add_argument("--remove", action="store_true", help="remove reports and dependencies")
    args = parser.parse_args()

    if args.install:
        install_dependencies()
    elif args.remove:
        remove_reports()
    else:
        generate_report()


if __name__ == "__main__":
    main()
