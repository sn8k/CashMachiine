# Development Tasks v0.1.2

Date: 2025-08-19

## Core Services
- [x] Implement `api-gateway` (FastAPI) with authentication and RBAC.
- [x] Build `orchestrator` to schedule daily and intraday jobs.
- [x] Develop `data-ingestion` service for market connectors and OHLCV normalization.
- [x] Create `strategy-engine` for signal generation and allocation targets.
- [x] Design `risk-engine` handling risk budgets, VaR/ES limits, and stop levels.
- [x] Implement `execution-engine` for order generation and broker aggregation.
- [x] Provide `backtester` for reproducible simulations and reports.
- [x] Build `ui` using Next.js/React/Tailwind for dashboards and actions.
- [x] Set up `db` schema using Postgres and Timescale; configure Redis for caching.
- [x] Integrate message bus (NATS or RabbitMQ) for events and logs.

## Observability
- [x] Standardize structured logging and expose Prometheus metrics.
- [x] Configure OpenTelemetry traces and Grafana dashboards.

## Data Model
- [x] Implement tables for users, goals, accounts, portfolios, positions, orders, executions, prices, signals, actions, risk_limits, metrics_daily, and backtests.

## Documentation
- [x] Expand `user_manual` with installation, usage, and architecture details.
- [x] Maintain `changelog` for every update with version and date.

## MVP Deliverables
- [ ] Implement `feasibility-calculator` service (API + UI) for goal feasibility calculations.
- [ ] Extend `actions` UI with checklist and export of orders.
- [ ] Generate HTML reports in `backtester` CLI.

Refer to [user_manual_2025-08-19.md](user_manual_2025-08-19.md) for installation and usage details.
