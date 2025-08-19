#!/bin/bash
# data-ingestion removal v0.5.3
echo "Removing data-ingestion service..."
pip uninstall yfinance ccxt psycopg2-binary pika -y >/dev/null
