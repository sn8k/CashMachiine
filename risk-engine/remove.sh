#!/bin/bash
# risk-engine removal v0.4.5 (2025-08-19)
set -e

echo "Removing risk-engine service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
rm -rf logs
