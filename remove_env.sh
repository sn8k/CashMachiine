#!/usr/bin/env bash
# remove_env.sh v0.1.0

set -e

pip uninstall -r "$(dirname "$0")/requirements.txt" -y
