#!/bin/bash
# strategy-engine removal v0.4.4

echo "Removing strategy-engine service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
