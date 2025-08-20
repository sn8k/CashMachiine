#!/bin/bash
# audit-log removal v0.1.0
echo "Removing audit-log service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
