"""Uniswap DeFi fetcher v0.1.0 (2025-08-20)"""
from datetime import datetime
from typing import List
import requests

from .base import OHLCV, OHLCVFetcher


class UniswapFetcher(OHLCVFetcher):
    """Fetch OHLCV data from Uniswap via The Graph."""

    venue = "UNISWAP"

    def __init__(self, endpoint: str = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2") -> None:
        self.endpoint = endpoint

    def fetch(self, symbol: str) -> List[OHLCV]:
        """Retrieve the latest daily OHLCV for a given pair address."""
        query = (
            "{"""\n"
            "  pairDayDatas(first:1, orderBy: date, orderDirection: desc, where:{pairAddress: \"%s\"}) {""""\n"
            "    date open high low close volumeUSD""""\n"
            "  }""""\n"
            "}""" % symbol.lower()
        )
        try:
            resp = requests.post(self.endpoint, json={"query": query}, timeout=10)
            resp.raise_for_status()
            payload = resp.json()["data"]["pairDayDatas"]
            if not payload:
                return []
            d = payload[0]
            ts = datetime.utcfromtimestamp(int(d["date"]))
            return [
                OHLCV(
                    symbol,
                    self.venue,
                    ts,
                    float(d["open"]),
                    float(d["high"]),
                    float(d["low"]),
                    float(d["close"]),
                    float(d["volumeUSD"]),
                )
            ]
        except requests.RequestException as exc:  # pragma: no cover - network errors
            raise RuntimeError(f"Uniswap fetch failed: {exc}") from exc
