#!/bin/bash
# install_db.sh v0.1.3 (2025-08-22)
set -e
psql "$@" -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
for file in db/migrations/*.sql; do
  echo "Applying $file"
  psql "$@" -f "$file"
done
for file in db/migrations/warehouse/*.sql; do
  echo "Applying $file"
  psql "$@" -f "$file"
done

php admin/db_check.php
