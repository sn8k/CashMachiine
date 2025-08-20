# User Manual v0.6.14

Date: 2025-08-20

This document will evolve into a comprehensive encyclopedia for the project.

## Installation
- Copy `.env.example` to `.env` and adjust values as needed, including `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB` and `RATE_LIMIT_PER_MINUTE`.
- Run `./setup_env.sh` (Linux/Mac) or `setup_env.cmd` (Windows) to install Python dependencies.
- Use `./remove_env.sh` or `remove_env.cmd` to uninstall these dependencies.
- Each service provides `install.sh` and `remove.sh` scripts.
- Backtester includes a dedicated `requirements.txt` to ensure image builds succeed.
- UI translation assets install with `ui/install_locales.sh` and remove with `ui/remove_locales.sh`.
- Install RabbitMQ with `./install_rabbitmq.sh` and remove it with `./remove_rabbitmq.sh`.
- Start all services with `docker-compose up -d` and stop them with `docker-compose down`.

## Usage
- Authenticate and interact with the API Gateway at `/goals` and `/actions`. Requests are scoped by the `tenant_id` embedded in JWT tokens.
- Rate limiting is enforced per IP via Redis; defaults to 100 requests per minute.
- Start the scheduler with `python orchestrator/main.py`.
- Data ingestion consumes events from the scheduler via RabbitMQ.
- Pass `--install` or `--remove` to service scripts for setup and teardown.
- The UI supports French and English; append `/en` to URLs to switch to English.
- The feasibility-calculator service exposes `/feasibility` to estimate CAGR, daily returns and probability of hitting a target based on capital, goal, deadline and risk profile.

## Offline & Notifications
- The UI and mobile app register service workers, cache data in localStorage and subscribe to push notifications through notification-service.

## Audit Log
- The `audit-log` service records domain events in the `audit_events` table.
- Replay state by selecting events ordered by `id` and republishing them with `common.events.emit_event`.

### Strategy Engine
- `strategy-engine` includes `simulation.py` for Monte Carlo path generation and probability-of-hitting analysis.
- Core and satellite strategies now consume market data, adjust risk via the risk engine, and explain target weights through `explain()`.

## Performance
- Run benchmarks with `pytest --benchmark-json=perf/<service>/results.json`.
- Benchmark tests cover `api-gateway` and `strategy-engine`.
- Prometheus exposes latency metrics on each service's metrics port.
- Benchmark results are stored under `perf/`.

## Architecture
- Services communicate via structured logs, metrics, and traces.
- Review the [README](README.md#6-architecture-technique) for the full technical specification.

## Continuous Integration
- The `ci.yml` workflow runs lint, tests and builds service images on each push or pull request.
- Badges in the README display the latest status for `lint`, `test` and `build` jobs.

## Security Policies
- The CI pipeline scans Python code with Bandit and frontend dependencies with `npm audit`.
- Dependency vulnerabilities cause the pipeline to fail, providing automatic alerts.
- Developers can run `bandit -r .` and `npm run audit` locally before pushing changes.

## Troubleshooting
- If dependencies are missing, rerun `./setup_env.sh`.
- Verify database connectivity with `php admin/db_check.php`.
- Check service logs under the `logs/` directory for error details.
- Ensure required variables are set in `.env`.

