#!/bin/bash
# data-ingestion installer v0.5.0
echo "Installing data-ingestion service..."
pip install yfinance ccxt psycopg2-binary pika >/dev/null
mkdir -p "$(dirname "$0")/logs"
