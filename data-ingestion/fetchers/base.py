"""Abstract fetcher base v0.1.2 (2025-08-20)"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List
import psycopg2

from config import settings

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
            host=settings.db_host,
            port=settings.db_port,
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_pass,
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


@dataclass
class MacroIndicator:
    indicator: str
    source: str
    value: float
    ts: datetime


class MacroFetcher(ABC):
    """Base class for macro-economic indicator fetchers."""

    @abstractmethod
    def fetch(self, *args, **kwargs) -> List[MacroIndicator]:
        """Fetch macro-economic indicators."""

    def save(self, records: List[MacroIndicator]) -> None:
        if not records:
            return
        conn = psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_pass,
        )
        with conn, conn.cursor() as cur:
            for r in records:
                cur.execute(
                    """
                    INSERT INTO macro_indicators(indicator, source, value, ts)
                    VALUES (%s,%s,%s,%s)
                    ON CONFLICT (indicator, source, ts) DO NOTHING
                    """,
                    (r.indicator, r.source, r.value, r.ts),
                )
        conn.close()
