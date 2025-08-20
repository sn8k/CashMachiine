# Changelog v0.6.51

## 2025-01-14
- Added Playwright end-to-end tests under `tests/e2e` for UI and API flows.
- Reports now output to `tests/e2e/reports/` with log scripts and `.gitignore` updated.
- Introduced `@playwright/test` dependency and Python `playwright` entry.
- Extended CI pipeline with an `e2e` job executing Playwright tests.
- Documented end-to-end testing in user manuals and created `user_manual_2025-01-14.md`.

## 2025-02-14
- Introduced user manual revision with installation, usage, architecture and troubleshooting sections.
- Cross-linked README and user manual.
- Bumped README to v0.1.1 and user manual/changelog to v0.6.0.

## 2025-08-19
- Added shared monitoring utilities providing JSON logging, Prometheus metrics and OpenTelemetry traces.
- Centralized logs under `logs/` with optional remote sink.
- Integrated monitoring into api-gateway, orchestrator and risk-engine services.
- Updated log creation scripts and `.gitignore` for new log paths.
- Documented monitoring setup in user manual.
- Added Prometheus and OpenTelemetry dependencies.
- Initialized Next.js UI with Tailwind pages for goal creation and daily actions referencing api-gateway.
- Removed binary UI screenshots and ignored image assets to comply with repository policy.
- Introduced GitHub Actions workflow running lint, tests and service image builds.
- Added CI status badges to README.
- Documented CI usage in user manuals.
- Introduced centralized configuration package loading `.env` files and environment variables.
- Added `.env.example` and referenced it in environment setup scripts.
- Updated services to consume `config` values instead of hard-coded constants.
- Added `python-dotenv` dependency.
- Introduced Redis cache infrastructure module with helpers.
- Added Redis-backed rate limiting middleware to api-gateway.
- Updated configuration, environment samples and documentation for Redis settings.
- Added `redis` and `fakeredis` dependencies.
- Added RabbitMQ-based messaging package with producers and consumers.
- Orchestrator now publishes events to the bus; data-ingestion consumes them.
- Added broker installer scripts and `pika` dependency with configuration.
- Added Dockerfiles for all services with version headers.
- Introduced root docker-compose.yml wiring services, database, cache and message bus.
- Updated setup/remove scripts to invoke `docker-compose up` and `docker-compose down`.
- Added data-warehouse module with nightly ETL and warehouse schema migrations.
- Logged ETL runs under `logs/data-warehouse/` and updated log creation scripts.
- Created warehouse migrations and updated `admin/db_check.php` for new tables.
- Updated root requirements with SQLAlchemy and refreshed documentation.
- Extended log creation scripts to include container log directories.
- Added Bandit and `npm audit` security scans to CI with automatic dependency alerts.
- Added Bandit dependency and UI `audit` script.
- Documented security policies in user manuals.
- Added analytics endpoint in api-gateway aggregating observability and database metrics.
- Created UI analytics dashboard fetching metrics from backend.
- Mirrored analytics SQL checks in `admin/db_check.php`.
- Extended log creation scripts for analytics logs.
- Updated documentation and README for analytics features.

- Introduced pytest-benchmark scripts for api-gateway and strategy-engine.
- Stored benchmark results under `perf/` and updated log creation scripts.
 Added Prometheus latency metrics via `setup_performance_metrics`.
 Documented benchmarking and metrics in user manual.
 Added `pytest-benchmark` dependency and ignored `perf/` artifacts.
- Marked development tasks as completed and linked documentation in user manuals.

- Implemented goals, actions and orders endpoints with a repository layer and admin-only mutations, and documented new APIs.

- Scheduled orchestrator pipeline dispatching `data_fetch`, `strategy_compute`, `risk_adjust` and `order_dispatch` events.
- Added EventConsumer entrypoints for strategy-engine, risk-engine and execution-engine.
- Renamed data-ingestion handler to `data_fetch`.
- Extended log creation scripts for new service log files.
- Bumped service versions and updated user manual for the event-driven workflow.
- Fixed service consumer imports by dropping hyphenated module paths.
- Addressed Bandit warnings with safe subprocess calls, test skips, and enhanced logging.

- Upgraded Next.js to 14.2.32 to resolve audit vulnerabilities and added a dedicated
  `messaging.log` path with version bumps across orchestrator and dependent services.

- Added per-service `requirements.txt` files with updated Dockerfiles and install scripts to eliminate build warnings.
 - Added Alpha Vantage bond and commodity fetchers with message bus integration.
 - Enabled TimescaleDB extension and converted `prices` to a hypertable with migration and schema checks.
 - Updated install script and documentation for TimescaleDB.

- Implemented real broker adapters using config-driven API keys and robust error handling.
- Order handler now stores orders and executions in the database with Redis caching.
- Updated log creation scripts and `.gitignore` for execution-engine order logs.
- Added unit tests for adapters and order handler using mocked requests and fakeredis.

- Introduced Terraform infrastructure modules for database, cache, message bus and services.
- Added `setup_tf.sh` and `teardown_tf.sh` with state and plan logs stored under `infra/terraform/logs/`.
- Extended log creation scripts and `.gitignore` for Terraform logs.
- Documented deployment procedure in user manuals.

- Added action checkboxes with status updates and feedback on the UI daily actions page.
- Rendered Chart.js metrics on the analytics dashboard with localized strings.
- Introduced Chart.js dependency and locale management scripts in `package.json`.
- Bumped locale installer scripts for updated translation assets.
- Documented new UI features and scripts in user manual.
- Silenced npm http-proxy warning in UI tests via `.npmrc` loglevel setting.

- Unified monitoring across order handler, data-ingestion and backtester with logging, metrics and tracing.
- Added Prometheus ports `9003` (execution-engine), `9004` (data-ingestion) and `9005` (backtester) with configuration entries.
- Extended log creation scripts for backtester logs.
- Documented new metrics endpoints in the user manual.
- Updated development tasks with new deliverables from the README and bumped README to v0.1.5 with current date linkage.
- Replaced insecure asserts in execution-engine tests and bound feasibility-calculator to localhost to satisfy Bandit.
- Added historical and hypothetical stress test endpoint `/risk/stress` with persistence, migrations and documentation.

- Scaffolded `notification-service` with `/notify/email` and `/notify/webhook` endpoints, RabbitMQ consumer,
 log directory, installer scripts and `notifications` table migration with schema checks.

- Made notification-service bind host configurable via environment variables to satisfy Bandit.
- Added database backup and restore scripts with configurable retention policy.
- Scheduled daily 02:00 backups via orchestrator and documented usage.
- Created `backups/` directory with log scripts and `.gitignore` updates.

- Scaffolded `strategy-marketplace` service with CRUD endpoints for uploaded strategies.
- Added `strategies` and `strategy_reviews` tables with migrations and schema checks.
- Stored uploaded strategy files under `strategy-marketplace/assets/` with dedicated log directory.
- Updated log creation scripts, `.gitignore` and documentation for the new service and installer scripts.

- Initialized React Native mobile app with install/remove scripts and build logging.
- Enabled PWA support in Next.js UI with service worker, manifest and offline cache.
- Added `logs/mobile/` path to log creation scripts for mobile build artifacts.
- Documented mobile and PWA features in user manuals.
- Reviewed development tasks, marking feasibility calculator, action UI export and backtester HTML reports as complete with cross-references in user manuals.
- Reconciled `development_tasks` with dated logs, adding deliverables for feasibility calculator documentation and backtester benchmarking.
- Updated user manuals with notes on feasibility calculator integration and backtester performance plans.

## 2025-08-18
- Added initial development tasks outline.
- Initialized user manual skeleton.
- Created first changelog entry.
- Scaffolded service directories with versioned bootstraps and scripts.
- Added .gitignore for build artifacts and volatile paths.
- Expanded user manual with service overview.
- Added requirements.txt with runtime and development dependencies.
- Introduced setup_env and remove_env scripts for Linux/Mac and Windows.
- Documented installer usage in user manuals.
- Added initial database schema migrations.
- Introduced admin/db_check.php for schema validation.
- Added install_db.sh and remove_db.sh scripts.
- Documented database setup in user manuals.
- Added FastAPI API gateway with JWT auth, role checks, version header, install scripts, tests, and updated requirements.
- Introduced orchestrator scheduler with APScheduler for daily 08:00 Europe/Paris jobs and configurable logging.
- Added log creation scripts for orchestrator logs.
- Updated user manual with scheduling details.
- Added APScheduler dependency to requirements.
- Updated orchestrator install/remove scripts to v0.3.0.
- Introduced modular Yahoo equities and Binance crypto fetchers with normalized OHLCV and DB storage.
- Added yfinance, ccxt and psycopg2-binary dependencies with installer updates.
- Extended log creation scripts and .gitignore for data-ingestion logs.
- Enhanced admin/db_check.php to validate `prices` table columns.
- Expanded user manual with data-ingestion fetcher usage.
- Added base Strategy interface with `signals()` and `target_weights()` methods.
- Introduced example `CoreStrategy` and `SatelliteStrategy` with unit-test stubs.
- Updated strategy-engine install/remove scripts to v0.3.0.
- Bumped requirements.txt to v0.2.4.
- Implemented risk-engine utilities for volatility targeting, VaR/ES limits, and Kelly caps with REST endpoint.
- Added strategy-engine client for risk service and tests for risk calculations.
- Updated risk-engine install/remove scripts to v0.3.0 and added log directories with script updates.
- Added numpy dependency and bumped requirements to v0.2.5.
- Expanded user manual with risk-engine usage and bumped to v0.5.4.
- Introduced broker-agnostic order handler with pluggable IBKR and Binance adapters.
- Logged orders in structured JSON and added execution-engine log directory.
- Updated log creation scripts and execution-engine install/remove to v0.3.0.
- Added execution-engine logs to .gitignore.
- Expanded user manual with execution-engine order handling and bumped to v0.5.5.
- Added backtester CLI for HTML reports with install/remove commands, tests, and report directories.
- Updated user manual and log creation scripts; ignored report outputs.

- Implemented database-driven price loading and portfolio simulation in backtester CLI with KPI charts.
- Stored backtest metrics in the `backtests` table and expanded schema checks.
- Added pandas and matplotlib dependencies with version bumps and updated tests and user manual.
- Introduced RandomForest-based price forecasting with model storage under `strategy-engine/models/` and scikit-learn dependency.

- Added fx-service for ECB-based FX conversions with `/convert` endpoint.
- Introduced `currency` columns on `accounts`, `orders`, `positions` and `executions` with migration and schema checks.
- Registered fx-service in docker-compose and log scripts.
- Documented currency conversion usage and bumped requirements.

## 2025-08-20
- Added Next.js internationalization with French default and English fallback locales.
- Externalized UI strings to translation files with locale install/remove scripts.
- Documented localization setup in user manuals.
- Added `requirements.txt` for backtester and bumped service to v0.3.2 fixing Docker builds.
- Added feasibility-calculator FastAPI service with `/feasibility` endpoint for CAGR, daily returns and probability-of-hitting calculations.
- Registered feasibility-calculator in docker-compose and log creation scripts and updated requirements and user manual.
- Introduced multi-tenant support with `tenant_id` columns on `users`, `goals` and `orders` tables.
- Extended JWT payloads and API gateway RBAC to enforce tenant scoping.
- Updated services to persist and query data by `tenant_id`.
- Documented tenant scoping in user manuals and bumped service versions.
- Introduced Monte Carlo simulation utilities in strategy-engine with probability-of-hitting calculations.
- Added interactive Windows installer `setup_full.cmd` with SQL database creation and `remove_full.cmd` for teardown; documented in user manual.
- Core and satellite strategies now derive signals from market data, adjust risk via the risk engine, and justify allocations through `explain()`.
- Extended strategy interface with `explain()` and added tests and documentation for dynamic weights.

- Added broker fee and tax calculations with DB columns and net order metrics returned by api-gateway.
- Added audit-log service capturing domain events in `audit_events` with producer helpers and replay docs.
- Implemented service workers and localStorage caches in mobile and UI.
- Integrated push notifications via notification-service and client APIs.
- Updated install scripts and log creation scripts for new components.
- Added Uniswap DeFi price fetcher and trade adapter with Web3 dependency, installer version bumps and new execution-engine logs; documented DeFi support in user manuals.
- Introduced reinforcement learning allocation optimizer using Stable Baselines3 with models saved under `strategy-engine/models/` and integrated `optimize_allocation` into the strategy workflow; updated log scripts and documentation.
- Scaffolded `kyc-service` FastAPI app for document uploads and status checks with Dockerfile, installers and log directories.
- Added `kyc_level` column migration on `users` with schema check updates and bumped expected DB version.
- Wired API gateway onboarding endpoints to proxy uploads and status queries to kyc-service.
- Expanded log creation scripts, docker-compose, environment samples, requirements and manuals for KYC integration.
- Added Locust performance tests for api-gateway and strategy-engine with CI integration and reports under `perf/`.
- Fixed Uniswap DeFi fetcher GraphQL query and updated documentation.
- Implemented OAuth2/OIDC login with Google and GitHub plus TOTP-based 2FA with backup codes.
- Added migration and schema checks for new auth columns and refreshed installers and requirements.
- Logged authentication events and updated log creation scripts and documentation.
- Moved OAuth token endpoints to configuration, replaced test asserts with explicit checks, and made KYC service host configurable.
