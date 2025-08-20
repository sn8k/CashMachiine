#!/bin/bash
# strategy-marketplace removal v0.3.2 (2025-08-20)
echo "Removing strategy-marketplace service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
