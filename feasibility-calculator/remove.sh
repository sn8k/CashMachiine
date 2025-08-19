#!/bin/bash
# feasibility-calculator removal v0.1.0 (2025-08-20)
set -e

echo "Removing feasibility-calculator service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
rm -rf logs
