#!/bin/bash
# orchestrator removal v0.5.3
echo "Removing orchestrator service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
