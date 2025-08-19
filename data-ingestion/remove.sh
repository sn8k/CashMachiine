#!/bin/bash
# data-ingestion removal v0.5.4
echo "Removing data-ingestion service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
