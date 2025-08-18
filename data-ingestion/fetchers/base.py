"""Abstract OHLCV fetcher base v0.1.0"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import os
from typing import List
import psycopg2

@dataclass
class OHLCV:
    symbol: str
    venue: str
    ts: datetime
    o: float
    h: float
    l: float
    c: float
    v: float

class OHLCVFetcher(ABC):
    """Base class for all OHLCV fetchers."""

    @abstractmethod
    def fetch(self, symbol: str) -> List[OHLCV]:
        """Fetch OHLCV data for a given symbol."""

    def save(self, records: List[OHLCV]) -> None:
        """Persist OHLCV records into the database."""
        if not records:
            return
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "cashmachiine"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "")
        )
        with conn, conn.cursor() as cur:
            for r in records:
                cur.execute(
                    """
                    INSERT INTO prices(symbol, venue, ts, o, h, l, c, v)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (symbol, venue, ts) DO NOTHING
                    """,
                    (r.symbol, r.venue, r.ts, r.o, r.h, r.l, r.c, r.v)
                )
        conn.close()
