#!/bin/bash
# data-ingestion removal v0.5.1
echo "Removing data-ingestion service..."
pip uninstall yfinance ccxt psycopg2-binary pika -y >/dev/null
