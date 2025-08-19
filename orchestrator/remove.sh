#!/bin/bash
# orchestrator removal v0.5.0
echo "Removing orchestrator service..."
pip uninstall pika -y >/dev/null
