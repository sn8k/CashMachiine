# Development Tasks v0.1.0

Date: 2025-08-18

## Core Services
- [ ] Implement `api-gateway` (FastAPI) with authentication and RBAC.
- [ ] Build `orchestrator` to schedule daily and intraday jobs.
- [ ] Develop `data-ingestion` service for market connectors and OHLCV normalization.
- [ ] Create `strategy-engine` for signal generation and allocation targets.
- [ ] Design `risk-engine` handling risk budgets, VaR/ES limits, and stop levels.
- [ ] Implement `execution-engine` for order generation and broker aggregation.
- [ ] Provide `backtester` for reproducible simulations and reports.
- [ ] Build `ui` using Next.js/React/Tailwind for dashboards and actions.
- [ ] Set up `db` schema using Postgres and Timescale; configure Redis for caching.
- [ ] Integrate message bus (NATS or RabbitMQ) for events and logs.

## Observability
- [ ] Standardize structured logging and expose Prometheus metrics.
- [ ] Configure OpenTelemetry traces and Grafana dashboards.

## Data Model
- [ ] Implement tables for users, goals, accounts, portfolios, positions, orders, executions, prices, signals, actions, risk_limits, metrics_daily, and backtests.

## Documentation
- [ ] Expand `user_manual` with installation, usage, and architecture details.
- [ ] Maintain `changelog` for every update with version and date.

