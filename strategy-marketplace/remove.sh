#!/bin/bash
# strategy-marketplace removal v0.3.0 (2025-08-19)
echo "Removing strategy-marketplace service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
