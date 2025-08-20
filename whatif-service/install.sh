#!/bin/bash
# whatif-service installer v0.3.1
echo "Installing whatif-service service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
mkdir -p "$(dirname "$0")/../logs/whatif-service"
