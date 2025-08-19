#!/bin/bash
# notification-service removal v0.3.1
echo "Removing notification-service service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
