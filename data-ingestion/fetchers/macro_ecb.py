"""ECB macro indicators fetcher v0.1.0 (2025-08-20)"""
from datetime import datetime, timezone
import requests

from .base import MacroFetcher, MacroIndicator


class ECBMacroFetcher(MacroFetcher):
    """Fetch euro area inflation from ECB SDW."""

    source = "ECB"

    def fetch(self) -> list[MacroIndicator]:
        url = "https://sdw.ecb.europa.eu/service/data/ICP/M.U2.N.000000.4.AV.A.CY"
        params = {"lastObs": 1, "format": "jsondata"}
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        try:
            value = float(data["dataSets"][0]["series"]["0:0:0:0:0"]["observations"]["0"][0])
        except Exception:
            return []
        ts = datetime.now(timezone.utc)
        return [MacroIndicator(indicator="HICP", source=self.source, value=value, ts=ts)]
