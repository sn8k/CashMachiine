#!/bin/bash
# orchestrator installer v0.5.5
echo "Installing orchestrator service..."
pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt >/dev/null
