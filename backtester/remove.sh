#!/bin/bash
# backtester removal v0.3.0 (2025-08-18)
echo "Removing backtester service..."
rm -rf "$(dirname "$0")/reports"
