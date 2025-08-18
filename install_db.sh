#!/bin/bash
# install_db.sh v0.1.0
set -e
for file in db/migrations/*.sql; do
  echo "Applying $file"
  psql "$@" -f "$file"
done
