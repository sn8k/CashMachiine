#!/bin/bash
# strategy-marketplace installer v0.3.0 (2025-08-19)
echo "Installing strategy-marketplace service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
mkdir -p "$(dirname "$0")/../logs/strategy-marketplace"
