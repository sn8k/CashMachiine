"""FRED macro indicators fetcher v0.1.0 (2025-08-20)"""
from datetime import datetime, timezone
import requests

from .base import MacroFetcher, MacroIndicator
from config import settings


class FREDMacroFetcher(MacroFetcher):
    """Fetch US indicators from FRED."""

    source = "FRED"

    def fetch(self, series_id: str = "GDP") -> list[MacroIndicator]:
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": series_id,
            "api_key": settings.fred_api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 1,
        }
        resp = requests.get(url, params=params, timeout=10)
        obs = resp.json().get("observations", [])
        if not obs:
            return []
        row = obs[0]
        try:
            value = float(row["value"])
        except Exception:
            return []
        ts = datetime.strptime(row["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return [MacroIndicator(indicator=series_id, source=self.source, value=value, ts=ts)]
