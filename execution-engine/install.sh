#!/bin/bash
# execution-engine installer v0.4.6 (2025-08-20)
set -e
mkdir -p "$(dirname \"$0\")/logs"
echo "Installing execution-engine service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
