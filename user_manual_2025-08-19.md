# User Manual v0.6.5

Date: 2025-08-19

This document will evolve into a comprehensive encyclopedia for the project.

## Overview
- Goal-based investment platform with daily actionable recommendations.
- Redis cache infrastructure provides shared helpers for services.

## Services Overview
- api-gateway
- orchestrator
- data-ingestion
- messaging
- strategy-engine
- risk-engine
- execution-engine
- backtester
- ui
- db
- infra/cache

## Installation
- Copy `.env.example` to `.env` and adjust values as needed.
- Set Redis config using `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB` and `RATE_LIMIT_PER_MINUTE`.
- Run `./setup_env.sh` (Linux/Mac) or `setup_env.cmd` (Windows) to install Python dependencies.
- Use `./remove_env.sh` or `remove_env.cmd` to uninstall these dependencies.
- Each service includes install.sh and remove.sh scripts (v0.3.0).
- Install RabbitMQ with `./install_rabbitmq.sh` and remove it with `./remove_rabbitmq.sh`.
- Start all services with `docker-compose up -d` and stop them with `docker-compose down`.

## Database Setup
- Run `./install_db.sh` to create tables.
- Run `./remove_db.sh` to drop tables.
- Verify with `php admin/db_check.php`.

## Monitoring
- Shared JSON logging writes to `logs/` with optional remote sink via `REMOTE_LOG_URL`.
- Prometheus metrics exposed per service on configurable `METRICS_PORT`.
- OpenTelemetry traces exported to console for debugging.

## Continuous Integration
- GitHub Actions `ci.yml` workflow runs lint, tests and builds service images.
- Status badges in the README show the latest pipeline results.

## Security Policies
- The CI pipeline scans Python code with Bandit and frontend dependencies with `npm audit`.
- Dependency vulnerabilities cause the pipeline to fail, providing automatic alerts.
- Developers can run `bandit -r .` and `npm run audit` locally before pushing changes.

## API Gateway
- FastAPI service exposing `/goals` for users and `/actions` for admins.
- Authenticate requests with JWT tokens containing a `role` claim.
- All responses include header `X-API-Version: v0.2.3`.
- Rate limiting enforced per IP using Redis; defaults to 100 requests/minute configurable via `RATE_LIMIT_PER_MINUTE`.
- Metrics default to port `9001`.
- Configuration values read from `config` package.

## Orchestrator
- Uses APScheduler to trigger daily jobs at 08:00 Europe/Paris and publishes events to RabbitMQ.
- Start with `python orchestrator/main.py`.
- Flags: `--install` to install, `--remove` to uninstall, `--log-path` to customize log file, `--metrics-port` for metrics.
- Default log file `logs/orchestrator.log`.

## Data Ingestion
- Modular fetchers for Yahoo equities and Binance crypto.
- Consumes RabbitMQ events and fetches data on demand.
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
- Configuration values read from `config` package.

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

## UI
- Next.js frontend with Tailwind CSS.
- `/goals` page submits new goals to the API Gateway `/goals` endpoint.
- `/daily-actions` page displays recommendations fetched from `/actions`.
- Install with `ui/install.sh` and remove with `ui/remove.sh` (v0.3.0).
- Screenshots:
  - Goal creation page (screenshot omitted)
  - Daily actions page (screenshot omitted)

