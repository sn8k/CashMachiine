#!/bin/bash
# install_db.sh v0.1.1 (2025-08-19)
set -e
psql "$@" -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
for file in db/migrations/*.sql; do
  echo "Applying $file"
  psql "$@" -f "$file"
done
