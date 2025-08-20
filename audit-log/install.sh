#!/bin/bash
# audit-log installer v0.1.0
echo "Installing audit-log service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
mkdir -p "$(dirname "$0")/logs"
