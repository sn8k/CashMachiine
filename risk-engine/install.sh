#!/bin/bash
# risk-engine installer v0.4.4 (2025-08-19)
set -e

echo "Installing risk-engine service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
mkdir -p logs
