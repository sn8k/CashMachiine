#!/bin/bash
# log directory creator v0.6.8 (2025-08-19)
set -e
mkdir -p logs
mkdir -p logs/containers
mkdir -p logs/analytics
mkdir -p backtester/reports
mkdir -p ui/.next
mkdir -p perf
mkdir -p execution-engine/logs
touch logs/orchestrator.log
touch logs/data-ingestion.log
touch logs/strategy-engine.log
touch logs/risk-engine.log
touch logs/execution-engine.log
touch logs/messaging.log
touch logs/feasibility-calculator.log
touch execution-engine/logs/orders.log
