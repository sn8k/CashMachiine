#!/usr/bin/env bash
# setup_env.sh v0.2.5 (2025-08-21)

set -e

pip install -r "$(dirname "$0")/requirements.txt"

if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
fi

rollback() {
  docker compose down 2>/dev/null || docker-compose down 2>/dev/null || true
}

wait_for_healthy() {
  local timeout=120
  local interval=5
  local elapsed=0
  while [ "$elapsed" -lt "$timeout" ]; do
    local status
    status=$(docker compose ps --format '{{.Service}} {{.Status}}' 2>/dev/null || docker-compose ps --format '{{.Service}} {{.Status}}')
    echo "$status"
    if echo "$status" | grep -q "unhealthy\|exited"; then
      echo "Detected unhealthy or exited container" >&2
      rollback
      exit 1
    fi
    if echo "$status" | grep -qv "running" || echo "$status" | grep -q "starting"; then
      sleep "$interval"
      elapsed=$((elapsed + interval))
      continue
    fi
    return 0
  done
  echo "Timeout waiting for containers to become healthy" >&2
  rollback
  exit 1
}

if command -v docker >/dev/null 2>&1; then
  docker compose up -d || docker-compose up -d
  wait_for_healthy
elif command -v docker-compose >/dev/null 2>&1; then
  docker-compose up -d
  wait_for_healthy
fi
