#!/bin/bash
# data-ingestion installer v0.3.0
echo "Installing data-ingestion service..."
pip install yfinance ccxt psycopg2-binary
mkdir -p "$(dirname "$0")/logs"
