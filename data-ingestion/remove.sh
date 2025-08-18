#!/bin/bash
# data-ingestion removal v0.3.0
echo "Removing data-ingestion service..."
pip uninstall yfinance ccxt psycopg2-binary -y
