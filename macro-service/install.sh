#!/bin/bash
# macro-service installer v0.1.0
echo "Installing macro-service service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
mkdir -p "$(dirname "$0")/../logs/macro-service"
