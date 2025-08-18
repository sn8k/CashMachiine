#!/usr/bin/env bash
# setup_env.sh v0.1.0

set -e

pip install -r "$(dirname "$0")/requirements.txt"
