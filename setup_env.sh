#!/usr/bin/env bash
# setup_env.sh v0.2.3 (2025-08-20)

set -e

pip install -r "$(dirname "$0")/requirements.txt"

if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
fi

if command -v docker >/dev/null 2>&1; then
  docker compose up -d || docker-compose up -d
elif command -v docker-compose >/dev/null 2>&1; then
  docker-compose up -d
fi
