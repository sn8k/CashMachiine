"""Alpha Vantage bonds fetcher v0.1.0 (2025-08-19)"""
from datetime import datetime, timezone
import requests

from .base import OHLCV, OHLCVFetcher
from config import settings


class AlphaVantageBondFetcher(OHLCVFetcher):
    """Fetch daily treasury yields from Alpha Vantage."""

    venue = "ALPHAVANTAGE"

    def fetch(self, symbol: str):
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TREASURY_YIELD",
            "interval": "daily",
            "apikey": settings.alpha_vantage_key,
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json().get("data", [])
        records: list[OHLCV] = []
        for row in data:
            ts = datetime.strptime(row["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            yld = float(row["value"])
            records.append(
                OHLCV(symbol=symbol, venue=self.venue, ts=ts, o=yld, h=yld, l=yld, c=yld, v=0.0)
            )
        return records
