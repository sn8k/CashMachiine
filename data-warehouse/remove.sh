#!/bin/bash
# data-warehouse removal v0.1.0 (2025-08-19)
echo "Removing data-warehouse service..."
pip uninstall -y -r requirements.txt >/dev/null 2>&1
