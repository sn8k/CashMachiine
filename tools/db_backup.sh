#!/bin/bash
# db backup utility v0.1.0 (2025-08-19)
set -e

RETENTION_DAYS=7
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --retention)
      shift
      RETENTION_DAYS="$1"
      ;;
    --install)
      mkdir -p "backups"
      exit 0
      ;;
    --remove)
      rm -rf "backups"
      exit 0
      ;;
    *)
      ARGS+=("$1")
      ;;
  esac
  shift
done

mkdir -p backups
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DUMP_FILE="backups/db_${TIMESTAMP}.sql"
pg_dump "${ARGS[@]}" > "$DUMP_FILE"
find backups -type f -name 'db_*.sql' -mtime +"$RETENTION_DAYS" -delete
