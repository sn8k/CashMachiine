#!/bin/bash
# strategy-engine installer v0.4.4

echo "Installing strategy-engine service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
