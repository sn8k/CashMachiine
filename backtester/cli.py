#!/usr/bin/env python3
"""backtester CLI v0.4.0 (2025-08-19)"""
import argparse
import base64
import json
import os
import shutil
import subprocess  # nosec B404
import sys
from datetime import datetime
from io import BytesIO

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psycopg2

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import settings

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

    symbols = config.get("symbols")
    if not symbols:
        raise ValueError("config must include 'symbols'")
    capital = float(config.get("initial_capital", 10_000))

    conn = psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_pass,
    )

    prices: dict[str, pd.Series] = {}
    for sym in symbols:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT ts, c FROM prices WHERE symbol=%s AND ts BETWEEN %s AND %s ORDER BY ts",
                (sym, start_date, end_date),
            )
            rows = cur.fetchall()
        if not rows:
            raise ValueError(f"No price data for {sym}")
        df = pd.DataFrame(rows, columns=["ts", sym]).set_index("ts")
        prices[sym] = df[sym]
    price_df = pd.DataFrame(prices).sort_index()
    returns = price_df.pct_change().dropna()
    weights = np.repeat(1 / len(symbols), len(symbols))
    portfolio_returns = (returns * weights).sum(axis=1)
    equity = (1 + portfolio_returns).cumprod() * capital

    days = (equity.index[-1] - equity.index[0]).days or 1
    years = days / 365.25
    cagr = (equity.iloc[-1] / capital) ** (1 / years) - 1
    sharpe = np.sqrt(252) * portfolio_returns.mean() / (portfolio_returns.std() or 1)
    running_max = equity.cummax()
    drawdown = (equity - running_max) / running_max
    max_dd = drawdown.min()
    kpis = {"CAGR": cagr, "Sharpe": sharpe, "MaxDrawdown": max_dd}

    fig, ax = plt.subplots()
    equity.plot(ax=ax)
    ax.set_title("Equity Curve")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    os.makedirs(REPORT_DIR, exist_ok=True)
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(REPORT_DIR, f"report_{timestamp}.html")

    html = (
        "<html><body><h1>Backtest Report</h1>"
        f"<p>Strategy: {config.get('name', 'unknown')}</p>"
        f"<p>Start: {start_date}</p>"
        f"<p>End: {end_date}</p>"
        "<h2>KPIs</h2><ul>"
        + "".join(f"<li>{k}: {v:.4f}</li>" for k, v in kpis.items())
        + "</ul>"
        f"<img src='data:image/png;base64,{img_b64}' alt='Equity Curve'/></body></html>"
    )

    with open(output_path, "w", encoding="utf-8") as out:
        out.write(html)
    print(f"Report generated at {output_path}")

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO backtests (cfg_json, start, end, kpis_json, report_path) VALUES (%s,%s,%s,%s,%s)",
            (json.dumps(config), start_date, end_date, json.dumps(kpis), output_path),
        )
        conn.commit()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Backtester controller v0.4.0")
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
