#!/bin/bash
# kyc-service installer v0.1.0 (2025-08-20)
echo "Installing kyc-service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
mkdir -p "$(dirname "$0")/../logs/kyc-service"
mkdir -p "$(dirname "$0")/uploads"
