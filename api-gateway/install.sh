#!/bin/bash
# api-gateway installer v0.3.1
echo "Installing api-gateway service dependencies..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
