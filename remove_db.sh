#!/bin/bash
# remove_db.sh v0.1.0
set -e
TABLES=(actions backtests metrics_daily risk_limits signals prices executions orders positions portfolios accounts goals users)
for tbl in "${TABLES[@]}"; do
  echo "Dropping $tbl"
  psql "$@" -c "DROP TABLE IF EXISTS $tbl CASCADE;"
done
