#!/bin/bash
# log directory creator v0.6.19 (2025-08-20)
set -e
mkdir -p logs
mkdir -p logs/containers
mkdir -p logs/analytics
mkdir -p backtester/reports
mkdir -p tests/e2e/reports
mkdir -p ui/.next
mkdir -p perf
mkdir -p execution-engine/logs
mkdir -p infra/terraform/logs
mkdir -p logs/notification-service
mkdir -p logs/strategy-marketplace
mkdir -p logs/fx-service
mkdir -p logs/mobile
mkdir -p logs/data-warehouse
mkdir -p strategy-engine/models
mkdir -p strategy-marketplace/assets
mkdir -p backups
mkdir -p logs/audit-log
touch logs/orchestrator.log
touch logs/data-ingestion.log
touch logs/strategy-engine.log
touch logs/risk-engine.log
touch logs/execution-engine.log
touch logs/messaging.log
touch logs/feasibility-calculator.log
touch logs/backtester.log
touch logs/notification-service/notification.log
touch logs/strategy-marketplace/marketplace.log
touch logs/fx-service/fx.log
touch execution-engine/logs/orders.log
touch logs/mobile/build.log
touch logs/data-warehouse/etl.log
touch logs/audit-log/audit.log
