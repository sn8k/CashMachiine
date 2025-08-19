# User Manual v0.5.7

Date: 2025-08-19

This document will evolve into a comprehensive encyclopedia for the project.

## Overview
- Goal-based investment platform with daily actionable recommendations.

## Services Overview
- api-gateway
- orchestrator
- data-ingestion
- strategy-engine
- risk-engine
- execution-engine
- backtester
- ui
- db

## Installation
- Run `./setup_env.sh` (Linux/Mac) or `setup_env.cmd` (Windows) to install Python dependencies.
- Use `./remove_env.sh` or `remove_env.cmd` to uninstall these dependencies.
- Each service includes install.sh and remove.sh scripts (v0.3.0).

## Database Setup
- Run `./install_db.sh` to create tables.
- Run `./remove_db.sh` to drop tables.
- Verify with `php admin/db_check.php`.

## Monitoring
- Shared JSON logging writes to `logs/` with optional remote sink via `REMOTE_LOG_URL`.
- Prometheus metrics exposed per service on configurable `METRICS_PORT`.
- OpenTelemetry traces exported to console for debugging.

## API Gateway
- FastAPI service exposing `/goals` for users and `/actions` for admins.
- Authenticate requests with JWT tokens containing a `role` claim.
- All responses include header `X-API-Version: v0.2.1`.
- Metrics default to port `9001`.

## Orchestrator
- Uses APScheduler to trigger daily jobs at 08:00 Europe/Paris.
- Start with `python orchestrator/main.py`.
- Flags: `--install` to install, `--remove` to uninstall, `--log-path` to customize log file, `--metrics-port` for metrics.
- Default log file `logs/orchestrator.log`.

## Data Ingestion
- Modular fetchers for Yahoo equities and Binance crypto.
- Example usage:
  - `from data_ingestion.fetchers.equities_yahoo import YahooEquityFetcher`
  - `YahooEquityFetcher().save(YahooEquityFetcher().fetch("AAPL"))`
- Logs stored in `logs/data-ingestion.log`.

## Strategy Engine
- Base `Strategy` interface exposing `signals()` and `target_weights()`.
- Example implementations: `CoreStrategy` and `SatelliteStrategy`.

## Risk Engine
- Provides volatility targeting, Value-at-Risk/Expected Shortfall checks, and Kelly fraction caps.
- REST endpoint `/adjust` consumed by `strategy-engine` via `risk_client`.
- Logs stored in `logs/risk-engine.log` and metrics default to port `9002`.

## Execution Engine
- Broker-agnostic `OrderHandler` with pluggable adapters (`IBKR`, `Binance`).
- Structured JSON order logs written to `logs/execution-engine.log`.
- Install with `execution-engine/install.sh` and remove with `execution-engine/remove.sh` (v0.3.0).

## Backtester
- Generate HTML performance reports from strategy configs.
- Run `python backtester/cli.py --config config.json --start-date 2024-01-01 --end-date 2024-06-01`.
- Use `--output` to specify report path; defaults to `backtester/reports`.
- Flags: `--install` to prepare report directory, `--remove` to clean it`.

## Architecture
- See README for initial specification.
