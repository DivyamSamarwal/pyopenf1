"""Optional in-memory TTL cache for API responses.

Certain OpenF1 data (e.g. completed race results, driver info) is immutable
once finalized, making it safe to cache aggressively.  This module provides
a simple async-safe LRU+TTL cache that can be plugged into
:class:`~pyopenf1.core.http_client.BaseHTTPClient`.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any


class TTLCache:
    """Async-safe in-memory cache with TTL expiry and LRU eviction.

    Args:
        default_ttl: Default time-to-live in seconds for cached entries.
        max_size: Maximum number of entries before the oldest is evicted.
    """

    def __init__(
        self,
        *,
        default_ttl: float = 300.0,
        max_size: int = 1024,
    ) -> None:
        self._default_ttl = default_ttl
        self._max_size = max_size
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Any | None:
        """Retrieve a cached value if it exists and has not expired.

        Args:
            key: Cache key (typically the full request URL with params).

        Returns:
            The cached value, or ``None`` if not found or expired.
        """
        async with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, expires_at = entry
            if time.monotonic() > expires_at:
                del self._store[key]
                return None
            return value

    async def set(self, key: str, value: Any, *, ttl: float | None = None) -> None:
        """Store a value in the cache.

        Args:
            key: Cache key.
            value: The value to cache.
            ttl: Time-to-live in seconds.  Falls back to ``default_ttl``.
        """
        effective_ttl = ttl if ttl is not None else self._default_ttl
        async with self._lock:
            # Evict oldest entries if at capacity
            while len(self._store) >= self._max_size:
                oldest_key = next(iter(self._store))
                del self._store[oldest_key]
            self._store[key] = (value, time.monotonic() + effective_ttl)

    async def clear(self) -> None:
        """Remove all entries from the cache."""
        async with self._lock:
            self._store.clear()

    def _make_key(self, method: str, path: str, params: dict[str, Any] | None = None) -> str:
        """Build a deterministic cache key from request components.

        Args:
            method: HTTP method.
            path: URL path.
            params: Query parameters.

        Returns:
            A stable string key.
        """
        sorted_params = sorted((params or {}).items())
        return f"{method}:{path}:{sorted_params}"
