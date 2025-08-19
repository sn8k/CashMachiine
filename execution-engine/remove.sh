#!/bin/bash
# execution-engine removal v0.4.4
set -e
echo "Removing execution-engine service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
