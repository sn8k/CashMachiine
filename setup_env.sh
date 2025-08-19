#!/usr/bin/env bash
# setup_env.sh v0.2.0

set -e

pip install -r "$(dirname "$0")/requirements.txt"

if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
fi
