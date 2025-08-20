#!/usr/bin/env bash
# remove_env.sh v0.1.2 (2025-08-20)

set -e

pip uninstall -r "$(dirname "$0")/requirements.txt" -y

if command -v docker >/dev/null 2>&1; then
  docker compose down || docker-compose down
elif command -v docker-compose >/dev/null 2>&1; then
  docker-compose down
fi
