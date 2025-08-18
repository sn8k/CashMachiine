"""Yahoo Finance equities fetcher v0.1.0"""
from datetime import timezone
import yfinance as yf
from .base import OHLCV, OHLCVFetcher

class YahooEquityFetcher(OHLCVFetcher):
    venue = "YAHOO"

    def fetch(self, symbol: str):
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d", interval="1d")
        records = []
        for idx, row in hist.iterrows():
            ts = idx.to_pydatetime().replace(tzinfo=timezone.utc)
            records.append(
                OHLCV(
                    symbol=symbol,
                    venue=self.venue,
                    ts=ts,
                    o=float(row["Open"]),
                    h=float(row["High"]),
                    l=float(row["Low"]),
                    c=float(row["Close"]),
                    v=float(row["Volume"]),
                )
            )
        return records
