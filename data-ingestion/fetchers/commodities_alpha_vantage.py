"""Alpha Vantage commodities fetcher v0.1.0 (2025-08-19)"""
from datetime import datetime, timezone
import requests

from .base import OHLCV, OHLCVFetcher
from config import settings


class AlphaVantageCommodityFetcher(OHLCVFetcher):
    """Fetch daily commodity prices from Alpha Vantage."""

    venue = "ALPHAVANTAGE"

    def fetch(self, symbol: str):
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": settings.alpha_vantage_key,
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json().get("Time Series (Daily)", {})
        records: list[OHLCV] = []
        for date_str, row in data.items():
            ts = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            records.append(
                OHLCV(
                    symbol=symbol,
                    venue=self.venue,
                    ts=ts,
                    o=float(row["1. open"]),
                    h=float(row["2. high"]),
                    l=float(row["3. low"]),
                    c=float(row["4. close"]),
                    v=float(row["5. volume"]),
                )
            )
            break
        return records
