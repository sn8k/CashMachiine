# Changelog v0.6.8

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
- Extended log creation scripts to include container log directories.
- Added Bandit and `npm audit` security scans to CI with automatic dependency alerts.
- Added Bandit dependency and UI `audit` script.
- Documented security policies in user manuals.

- Introduced pytest-benchmark scripts for api-gateway and strategy-engine.
- Stored benchmark results under `perf/` and updated log creation scripts.
 Added Prometheus latency metrics via `setup_performance_metrics`.
 Documented benchmarking and metrics in user manual.
 Added `pytest-benchmark` dependency and ignored `perf/` artifacts.

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

## 2025-08-20
- Added Next.js internationalization with French default and English fallback locales.
- Externalized UI strings to translation files with locale install/remove scripts.
- Documented localization setup in user manuals.
- Added `requirements.txt` for backtester and bumped service to v0.3.2 fixing Docker builds.

