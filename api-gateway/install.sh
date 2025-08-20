#!/bin/bash
# api-gateway installer v0.3.0
echo "Installing api-gateway service dependencies..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
