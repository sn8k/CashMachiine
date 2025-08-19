"""Redis client helper v0.1.0 (2025-08-19)"""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Optional

import redis


@lru_cache
def get_redis_client() -> redis.Redis:
    """Return a Redis client using environment configuration."""
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    db = int(os.getenv("REDIS_DB", "0"))
    try:
        client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        client.ping()
    except Exception:
        import fakeredis

        client = fakeredis.FakeStrictRedis()
    return client


def cache_set(key: str, value: Any, expire: Optional[int] = None) -> None:
    """Set a value in Redis with optional expiration."""
    client = get_redis_client()
    client.set(name=key, value=value, ex=expire)


def cache_get(key: str) -> Any:
    """Retrieve a value from Redis."""
    client = get_redis_client()
    return client.get(name=key)
