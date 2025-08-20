#!/bin/bash
# notification-service installer v0.3.2 (2025-08-20)
echo "Installing notification-service service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
mkdir -p "$(dirname "$0")/../logs/notification-service"
