#!/bin/bash
# remove_db.sh v0.1.2 (2025-08-20)
set -e
TABLES=(actions backtests metrics_daily risk_anomalies risk_limits signals prices executions orders positions portfolios accounts goals users audit_events)
for tbl in "${TABLES[@]}"; do
  echo "Dropping $tbl"
  psql "$@" -c "DROP TABLE IF EXISTS $tbl CASCADE;"
done
