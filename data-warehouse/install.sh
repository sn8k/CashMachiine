#!/bin/bash
# data-warehouse installer v0.1.0 (2025-08-19)
echo "Installing data-warehouse service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
mkdir -p logs/data-warehouse
