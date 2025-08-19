#!/bin/bash
# data-ingestion installer v0.5.4
echo "Installing data-ingestion service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
mkdir -p "$(dirname "$0")/logs"
