# User Manual v0.6.36

Date: 2025-08-19

This document will evolve into a comprehensive encyclopedia for the project.

## Development Roadmap
- Refer to [development_tasks.md](development_tasks.md) for the latest task status.

## Installation
- Copy `.env.example` to `.env` and adjust values as needed, including `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, `RATE_LIMIT_PER_MINUTE`, `ALPHA_VANTAGE_KEY`, `BINANCE_API_KEY`, `BINANCE_API_SECRET` and `IBKR_API_KEY`.
- Run `./setup_env.sh` (Linux/Mac) or `setup_env.cmd` (Windows) to install Python dependencies.
- Use `./remove_env.sh` or `remove_env.cmd` to uninstall these dependencies.
- Each service provides `install.sh` and `remove.sh` scripts.
- Each service now ships with its own `requirements.txt` for Docker builds.
- Backtester includes a dedicated `requirements.txt` to ensure image builds succeed.
- UI translation assets install with `ui/install_locales.sh` or `npm run locales:install` and remove with `ui/remove_locales.sh` or `npm run locales:remove`.
- Mobile dependencies install with `mobile/install.sh` and remove with `mobile/remove.sh`; build logs output to `logs/mobile/`.
- Install RabbitMQ with `./install_rabbitmq.sh` and remove it with `./remove_rabbitmq.sh`.
- Start all services with `docker-compose up -d` and stop them with `docker-compose down`.
- Run `./install_db.sh` to apply migrations; the script enables TimescaleDB and converts `prices` to a hypertable.
- Create PostgreSQL dumps with `tools/db_backup.sh --retention <days>` (default 7) which stores files under `backups/` and prunes old ones.
- Restore a dump via `tools/db_restore.sh <dump_file>`.
- `npm test` now runs without legacy proxy warnings thanks to a local `.npmrc`.
- Install Playwright browsers with `npm run install:e2e` and remove them with `npm run remove:e2e`.
- Execute end-to-end tests via `npm run test:e2e`; reports are written to `tests/e2e/reports/`.

## Infrastructure Deployment
- Modules for database, cache, message bus and services live under `infra/terraform/`.
- Execute `./setup_tf.sh` to initialize, plan and apply Terraform, storing state and plan logs in `infra/terraform/logs/`.
- Use `./teardown_tf.sh` to destroy deployed resources, writing output to the same log directory.

## Progressive Web App
- The Next.js UI registers a service worker and offline cache via `next-pwa`.
- A web app manifest lives at `ui/public/manifest.json`.

## Mobile Application
- React Native app initialized under `mobile/` with a simple entry point.
- Use `mobile/build.sh` to generate mobile build logs in `logs/mobile/`.

## Usage
- Authenticate and interact with the API Gateway at `/goals`, `/goals/{id}/status`, `/actions/today`, `/actions/{id}/check` and `/orders/preview`. Requests are scoped by the `tenant_id` embedded in JWT tokens.
- POST endpoints require the `admin` role.
- Rate limiting is enforced per IP via Redis; defaults to 100 requests per minute.
- Start the scheduler with `python orchestrator/main.py`.
 - The orchestrator sequentially dispatches `data_fetch`, `strategy_compute`, `risk_adjust` and `order_dispatch` events.
 - A daily 02:00 backup job invokes `tools/db_backup.sh`.
 - `data_fetch` covers equities, bonds and commodities via Alpha Vantage fetchers.
- Data ingestion, strategy-engine, risk-engine and execution-engine consume these events from RabbitMQ.
- The notification-service offers `/notify/email` and `/notify/webhook`, consumes `notifications` events and logs to `logs/notification-service/`.
- The strategy-marketplace service exposes CRUD endpoints at `/strategies` and stores uploads under `strategy-marketplace/assets/`.
- Configure its binding via `NOTIFICATION_HOST` (default `127.0.0.1`) and `NOTIFICATION_PORT`.
- Execution-engine adapters pull API keys from configuration (`BINANCE_API_KEY`, `BINANCE_API_SECRET`, `IBKR_API_KEY`). Orders
  are persisted to `orders` and `executions` tables, cached in Redis and logged to `execution-engine/logs/orders.log`.
- Pass `--install` or `--remove` to service scripts for setup and teardown.
- The UI supports French and English; append `/en` to URLs to switch to English.
- Mark tasks complete on the daily actions page; checkboxes send POST requests to `/actions/{id}/check` and show feedback messages.
- Visualize aggregated metrics via the `/analytics` endpoint or the UI analytics page, which renders charts with Chart.js.
- The feasibility-calculator service exposes `/feasibility` to estimate CAGR, daily returns and probability of hitting a target based on capital, goal, deadline and risk profile.
- It now binds to `127.0.0.1` by default for improved security.
- The backtester CLI loads prices from the database, simulates equal-weight portfolios, computes KPIs (CAGR, Sharpe, max drawdown), embeds equity charts in HTML reports and records metrics in the `backtests` table.
- Risk engine additionally offers `/risk/stress` for historical and hypothetical scenario analysis with stored results.

### Strategy Engine
- `strategy-engine` now provides `simulation.py` for Monte Carlo path generation and probability-of-hitting analysis.
- Core and satellite strategies consume market data, call the risk engine for adjustments, and expose `explain()` for weight justification.
- `ml_forecast.py` supplies `forecast_prices()` using RandomForest models stored in `strategy-engine/models/`.

## Performance
- Run benchmarks with `pytest --benchmark-json=perf/<service>/results.json`.
- Benchmark tests cover `api-gateway` and `strategy-engine`.
- Prometheus exposes latency metrics on each service's metrics port.
- Metrics endpoints:
  - API Gateway: `http://localhost:9001/metrics`
  - Risk Engine: `http://localhost:9002/metrics`
  - Execution Engine: `http://localhost:9003/metrics`
  - Data Ingestion: `http://localhost:9004/metrics`
  - Backtester: `http://localhost:9005/metrics`
- Benchmark results are stored under `perf/`.

## Architecture
- Services communicate via structured logs, metrics, and traces.
- Review the [README](README.md#6-architecture-technique) for the full technical specification.

## Continuous Integration
- The `ci.yml` workflow runs lint, tests and builds service images on each push or pull request.
- Badges in the README display the latest status for `lint`, `test` and `build` jobs.
- A dedicated job executes Playwright end-to-end tests and stores HTML reports under `tests/e2e/reports/`.

## Security Policies
- The CI pipeline scans Python code with Bandit and frontend dependencies with `npm audit`.
- Dependency vulnerabilities cause the pipeline to fail, providing automatic alerts.
- Developers can run `bandit -r .` and `npm run audit` locally before pushing changes.
- Tests use `# nosec` to bypass false positives and subprocess calls are validated.
- The UI now runs on Next.js 14.2.32 following security advisories.

## Troubleshooting
- If dependencies are missing, rerun `./setup_env.sh`.
- Verify database connectivity with `php admin/db_check.php`.
- Check service logs under the `logs/` directory for error details.
- Ensure required variables are set in `.env`.
- If Python raises syntax errors for imports with hyphens, replace them with underscores or use relative imports.
- Messaging events write to `logs/messaging.log` for debugging bus traffic.

