#!/bin/bash
# macro-service removal v0.1.0
echo "Removing macro-service service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
