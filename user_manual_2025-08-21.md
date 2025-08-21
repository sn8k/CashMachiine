# User Manual v0.6.91
=======


Date: 2025-08-21

This document will evolve into a comprehensive encyclopedia for the project.

## Development Roadmap
- Refer to [development_tasks_2025-08-20.md](development_tasks_2025-08-20.md) for the latest task status.

## Installation
- Prerequisites:
  - Python
  - pip
  - PostgreSQL `psql`
  - Docker
  - Node.js
- `setup_full.cmd` checks for these tools, prompts for database, RabbitMQ, API Gateway and API keys, writing values to `.env`, and opens download pages if any are missing. If `psql` or TimescaleDB is unavailable, it pulls and starts a `timescale/timescaledb` container with your credentials. Before applying migrations it dumps the current database to `backups/`. The script writes all output to `logs\\setup_full.log` and accepts a `--silent` flag or `--config <file>` to skip prompts. After prompts it creates `.env` if missing, replaces database placeholders with the provided values, creates the database role if needed and grants it privileges on the target database.
- Copy `.env.example` to `.env` and adjust values as needed, including `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, `RATE_LIMIT_PER_MINUTE`, `ALPHA_VANTAGE_KEY`, `BINANCE_API_KEY`, `BINANCE_API_SECRET`, `IBKR_API_KEY` and `FRED_API_KEY`.
- `DB_SCHEMA_VERSION` records the expected database schema revision (`v0.1.7`) checked by `admin/db_check.php`.
- Configure OAuth token endpoints via `GOOGLE_TOKEN_URL` and `GITHUB_TOKEN_URL` if overriding defaults.
- Set `KYC_HOST` to control the bind address of the KYC service (defaults to `127.0.0.1`).
- Run `./setup_env.sh` (Linux/Mac) or `setup_env.cmd` (Windows) to install Python dependencies; the Windows script now invokes `tools\\log_create_win.cmd` to create log directories.
- Use `./remove_env.sh` or `remove_env.cmd` to uninstall these dependencies.
- Run `setup_full.cmd` for an interactive Windows setup including database creation and a Python virtual environment; it now records service URLs and API keys in `.env`, invokes `tools\\log_create_win.cmd` at startup, installs UI dependencies and builds the frontend. The script rolls back on any failure by dropping the database, uninstalling dependencies and stopping containers while logging errors to `logs\setup_full.log`. Use `--silent` to accept defaults, `--config <file>` to supply answers, or `--seed` to execute SQL seed files without prompting. All output is logged to `logs\setup_full.log`. Use `remove_full.cmd` with the same flags to uninstall, remove the environment, drop the database, purge these credentials, delete UI `node_modules` and `.next` directories, and stop and remove the TimescaleDB container. Both scripts capture the database password with a PowerShell `Read-Host -AsSecureString` prompt instead of `set /p`, hiding the input.
- After base migrations, `setup_full.cmd` applies warehouse schema migrations from `db/migrations/warehouse/*.sql`.
- After migrations, `setup_full.cmd` can optionally execute seed SQL files from `db/seeds/*.sql` (admin user, demo accounts) to populate sample data.
- The script then verifies the database schema with `php admin\\db_check.php` and aborts if inconsistencies are found.
- Each service provides `install.sh` and `remove.sh` scripts.
- Each service now ships with its own `requirements.txt` for Docker builds.
- Requirements now include `web3` for on-chain interactions.
- Backtester includes a dedicated `requirements.txt` to ensure image builds succeed.
- UI translation assets install with `ui/install_locales.sh` or `npm run locales:install` and remove with `ui/remove_locales.sh` or `npm run locales:remove`.
- Mobile dependencies install with `mobile/install.sh` and remove with `mobile/remove.sh`; build logs output to `logs/mobile/`.
- Install RabbitMQ with `./install_rabbitmq.sh` and remove it with `./remove_rabbitmq.sh`.
- Start all services with `docker-compose up -d` and stop them with `docker-compose down`.
- Setup scripts wait for Docker containers to report healthy status and roll back if any container fails.
- Run `./install_db.sh` to apply migrations; the script enables TimescaleDB and converts `prices` to a hypertable.
- Create PostgreSQL dumps with `tools/db_backup.sh --retention <days>` (default 7) which stores files under `backups/` and prunes old ones.
- Restore a dump via `tools/db_restore.sh <dump_file>`.
- `npm test` now runs without legacy proxy warnings thanks to a local `.npmrc`.
- Install Playwright browsers with `npm run install:e2e` and remove them with `npm run remove:e2e`.
- Execute end-to-end tests via `npm run test:e2e`; tests rely on local mocks so no external network is required and reports are written to `tests/e2e/reports/`.
- Install the KYC service with `kyc-service/install.sh` and remove it with `kyc-service/remove.sh`.
- Install the macro-service with `macro-service/install.sh` and remove it with `macro-service/remove.sh`.

## Authentication
- OAuth2/OIDC login is available via Google and GitHub.
- Enable TOTP-based 2FA under `/auth/2fa/setup` and verify with `/auth/2fa/verify`.
- Backup codes are returned on setup and can be used through `/auth/2fa/recover` if the authenticator is lost.

## Infrastructure Deployment
- Modules for database, cache, message bus and services live under `infra/terraform/`.
- Execute `./setup_tf.sh` to initialize, plan and apply Terraform, storing state and plan logs in `infra/terraform/logs/`.
- Use `./teardown_tf.sh` to destroy deployed resources, writing output to the same log directory.

## Progressive Web App
- The Next.js UI registers a service worker for offline caching, stores daily actions in localStorage and subscribes to push notifications via notification-service.
- A web app manifest lives at `ui/public/manifest.json`.

## Mobile Application
- React Native app initializes under `mobile/`, registers a service worker when available, caches a welcome message in localStorage and subscribes to push notifications via notification-service.
- Use `mobile/build.sh` to generate mobile build logs in `logs/mobile/`.
- Orders now store `fee` and `tax` columns with strategy-engine utilities computing broker costs.
- API Gateway `/orders/preview` endpoint returns gross and net totals including fees and taxes.

## Data Warehouse
- Nightly ETL scripts load operational data into an analytical `warehouse` schema.
- Logs reside in `logs/data-warehouse/etl.log`.
- Install with `data-warehouse/install.sh` and remove with `data-warehouse/remove.sh` (v0.1.0).

## Audit Log
- The `audit-log` service consumes RabbitMQ events and stores them in the `audit_events` table.
- Replay system state by fetching events ordered by `id` and re-emitting them via `common.events.emit_event`.

## Usage
- Authenticate and interact with the API Gateway at `/goals`, `/goals/{id}/status`, `/actions/today`, `/actions/{id}/check` and `/orders/preview`. Requests are scoped by the `tenant_id` embedded in JWT tokens.
- POST endpoints require the `admin` role.
- Rate limiting is enforced per IP via Redis; defaults to 100 requests per minute.
- Start the scheduler with `python orchestrator/main.py`.
 - The orchestrator sequentially dispatches `data_fetch`, `strategy_compute`, `risk_adjust` and `order_dispatch` events.
 - A daily 02:00 backup job invokes `tools/db_backup.sh`.
 - Intraday monitoring checks volatility and drawdown every 5 minutes using cryptographically secure randomness and emits `volatility_alert` or `drawdown_alert` events to strategy-engine and execution-engine. Alerts are logged by `audit-log`.
- `data_fetch` covers equities, bonds, commodities and macro indicators via Alpha Vantage, ECB and FRED fetchers and on-chain DeFi prices from Uniswap.
- The Uniswap fetcher now leverages The Graph's `pairDayDatas` for more reliable OHLCV data.
- Data ingestion, strategy-engine, risk-engine and execution-engine consume these events from RabbitMQ.
- The notification-service offers `/notify/email` and `/notify/webhook`, consumes `notifications` events and logs to `logs/notification-service/`.
- Subscribe to risk alerts via `/alerts/subscribe`; the alert-engine consumes risk metrics and logs entries in the `alerts` table.
- The strategy-marketplace service exposes CRUD endpoints at `/strategies` and stores uploads under `strategy-marketplace/assets/`.
- Uploaded strategies can now run inside isolated Docker containers with signature verification and resource quotas. Execution results log to `logs/strategy-marketplace/executions.log`.
- Configure its binding via `NOTIFICATION_HOST` (default `127.0.0.1`) and `NOTIFICATION_PORT`.
- Execution-engine adapters pull API keys from configuration (`BINANCE_API_KEY`, `BINANCE_API_SECRET`, `IBKR_API_KEY`) and support on-chain swaps through a Uniswap adapter using Web3. Orders are persisted to `orders` and `executions` tables, cached in Redis and logged to `execution-engine/logs/orders.log`.
- Pass `--install` or `--remove` to service scripts for setup and teardown.
- The UI supports French and English; append `/en` to URLs to switch to English.
- Mark tasks complete on the daily actions page; checkboxes send POST requests to `/actions/{id}/check` and show feedback messages.
- The daily actions checklist also allows exporting orders for external processing.
- Visualize aggregated metrics via the `/analytics` endpoint or the UI analytics page, which renders charts with Chart.js.
- A `/ws` WebSocket endpoint streams `action`, `order` and `metrics` events; the UI consumes this feed to update pages in real time.
- The feasibility-calculator service exposes `/feasibility` to estimate CAGR, daily returns and probability of hitting a target based on capital, goal, deadline and risk profile.
- The whatif-service provides `/scenarios/run` and `/scenarios/{id}` endpoints to run scenarios and retrieve stored results in the `scenario_results` table.
- It now binds to `127.0.0.1` by default for improved security.
- Work in progress: integrate results into the UI overview, document the workflow and add automated tests.
- Generate consolidated PDF reports with `python reporting/generate_report.py`, which installs dependencies with `--install`, removes them with `--remove`, uses the active Python interpreter for `pip` operations and writes files to `reports/`.
- Upload identity documents via API Gateway `/onboard`; files are forwarded to kyc-service and stored under `kyc-service/uploads/`.
- Check verification progress at `/kyc/status/{user_id}`.
- The backtester CLI loads prices from the database, simulates equal-weight portfolios, computes KPIs (CAGR, Sharpe, max drawdown), embeds equity charts in HTML reports and records metrics in the `backtests` table.
- Planned: add performance benchmarking for simulations.
- Risk engine additionally offers `/risk/stress` for historical and hypothetical scenario analysis with stored results.
- Risk engine now detects anomalies in `metrics_daily` with an IsolationForest, logs them to `risk_anomalies`, and publishes `risk_anomaly` events to alert-engine.

### Strategy Engine
- `strategy-engine` now provides `simulation.py` for Monte Carlo path generation and probability-of-hitting analysis.
- Core and satellite strategies consume market data, call the risk engine for adjustments, and expose `explain()` for weight justification.
- `ml_forecast.py` supplies `forecast_prices()` using RandomForest models stored in `strategy-engine/models/`.
- `rl_optimizer.py` exposes a lightweight `optimize_allocation()` heuristic that scales allocation with recent returns; no external models are required.

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
- Execute Locust scenarios with `./tests/perf/run_perf.sh`, which automatically starts the API gateway and a risk engine instance on port 8001, producing HTML and CSV reports under `perf/reports/`.
- The script raises `RATE_LIMIT_PER_MINUTE` to `1000` during benchmarks to prevent rate limit errors.
- Custom scenario tasks emit stats via `events.request` because `request_success` hooks were removed in recent Locust versions.
- API Gateway average response time must remain under **500 ms**.
- Strategy Engine computation time must remain under **100 ms**.

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
- Randomness and subprocess usage across services are hardened to satisfy Bandit checks.
- The UI now runs on Next.js 14.2.32 following security advisories.

## fx-service
- Provides currency conversions using European Central Bank rates.
- POST `/convert` with JSON `{ "from_currency": "USD", "to_currency": "EUR", "amount": 1.23 }`.
- Returns converted amount and rate.
- Install with `fx-service/install.sh` and remove with `fx-service/remove.sh`.

## Troubleshooting
- If dependencies are missing, rerun `./setup_env.sh`.
- Verify database connectivity with `php admin/db_check.php`.
- Check service logs under the `logs/` directory for error details.
- Ensure required variables are set in `.env`.
- If Python raises syntax errors for imports with hyphens, replace them with underscores or use relative imports.
- Messaging events write to `logs/messaging.log` for debugging bus traffic.
- Risk-engine starts even if Prometheus or OpenTelemetry packages are absent; metrics and tracing are then disabled.
