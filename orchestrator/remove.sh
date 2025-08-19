#!/bin/bash
# orchestrator removal v0.4.0
echo "Removing orchestrator service..."
pip uninstall pika -y >/dev/null
