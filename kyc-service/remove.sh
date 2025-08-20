#!/bin/bash
# kyc-service removal v0.1.0 (2025-08-20)
echo "Removing kyc-service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
