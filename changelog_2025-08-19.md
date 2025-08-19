# Changelog v0.6.22

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
- Added analytics endpoint in api-gateway aggregating observability and database metrics.
- Created UI analytics dashboard fetching metrics from backend.
- Mirrored analytics SQL checks in `admin/db_check.php`.
- Extended log creation scripts for analytics logs.
- Updated documentation and README for analytics features.
- Reconciled development_tasks with repository state, marking tasks complete and cross-linking with user manual.
- Updated development tasks with new deliverables from the README and bumped README to v0.1.5 with current date linkage.

- Implemented goals, actions and orders endpoints with a repository layer and admin-only mutations, and documented new APIs.

- Implemented real broker adapters using config-driven API keys and robust error handling.
- Order handler now stores orders and executions in the database with Redis caching.
- Updated log creation scripts and `.gitignore` for execution-engine order logs.
- Added unit tests for adapters and order handler using mocked requests and fakeredis.

- Added action checkboxes with status updates and feedback on the UI daily actions page.
- Rendered Chart.js metrics on the analytics dashboard with localized strings.
- Introduced Chart.js dependency and locale management scripts in `package.json`.
- Bumped locale installer scripts for updated translation assets.
- Documented new UI features and scripts in user manual.

- Fixed service consumer imports by dropping hyphenated module paths.
- Addressed Bandit warnings with safe subprocess calls, test skips, and enhanced logging.

- Upgraded Next.js to 14.2.32 to resolve audit vulnerabilities and added a dedicated
  `messaging.log` path with version bumps across orchestrator and dependent services.

- Added per-service `requirements.txt` files with updated Dockerfiles and install scripts to eliminate build warnings.

- Implemented database-driven price loading and portfolio simulation in backtester CLI with KPI charts and metrics storage.
- Expanded `admin/db_check.php` to validate `backtests` columns and updated documentation with new dependencies.
- Silenced npm http-proxy warning in UI tests via `.npmrc` loglevel setting.


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

- Added Alpha Vantage bond and commodity fetchers with message bus integration.
- Enabled TimescaleDB extension and converted `prices` to a hypertable with migration and schema checks.
- Updated install script and documentation for TimescaleDB.

