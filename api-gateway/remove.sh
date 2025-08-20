#!/bin/bash
# api-gateway removal v0.2.9
echo "Removing api-gateway service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
