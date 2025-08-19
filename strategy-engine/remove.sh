#!/bin/bash
# strategy-engine removal v0.3.0

echo "Removing strategy-engine service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
