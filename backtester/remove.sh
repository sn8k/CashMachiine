#!/bin/bash
# backtester removal v0.4.0 (2025-08-19)
echo "Removing backtester service..."
rm -rf "$(dirname "$0")/reports"
