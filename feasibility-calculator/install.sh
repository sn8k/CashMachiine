#!/bin/bash
# feasibility-calculator installer v0.1.0 (2025-08-20)
set -e

echo "Installing feasibility-calculator service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
mkdir -p logs
