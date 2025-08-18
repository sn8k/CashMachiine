"""Binance crypto fetcher v0.1.0"""
from datetime import datetime
import ccxt
from .base import OHLCV, OHLCVFetcher

class BinanceCryptoFetcher(OHLCVFetcher):
    venue = "BINANCE"

    def __init__(self):
        self.exchange = ccxt.binance()

    def fetch(self, symbol: str):
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe="1d", limit=1)
        records = []
        for ts, o, h, l, c, v in ohlcv:
            dt = datetime.utcfromtimestamp(ts / 1000)
            records.append(OHLCV(symbol, self.venue, dt, float(o), float(h), float(l), float(c), float(v)))
        return records
