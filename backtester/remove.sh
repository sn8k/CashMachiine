#!/bin/bash
# backtester removal v0.3.2 (2025-08-20)
echo "Removing backtester service..."
rm -rf "$(dirname "$0")/reports"
