#!/bin/bash
# whatif-service removal v0.3.1
echo "Removing whatif-service service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
