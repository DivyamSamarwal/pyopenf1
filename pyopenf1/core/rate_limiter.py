"""Client-side rate limiter using a sliding-window token bucket.

Prevents the client from exceeding the OpenF1 rate limits
(free tier: 3 req/s and 30 req/min) *before* a 429 is returned,
reducing wasted round-trips.
"""

from __future__ import annotations

import asyncio
import time


class RateLimiter:
    """Async-safe sliding-window rate limiter.

    The limiter enforces two independent constraints:

    * **per-second**: at most ``max_per_second`` requests in any 1-second window.
    * **per-minute**: at most ``max_per_minute`` requests in any 60-second window.

    Args:
        max_per_second: Maximum requests allowed per second.
        max_per_minute: Maximum requests allowed per minute.
    """

    def __init__(
        self,
        *,
        max_per_second: float = 3.0,
        max_per_minute: float = 30.0,
    ) -> None:
        self._max_per_second = max_per_second
        self._max_per_minute = max_per_minute
        self._timestamps: list[float] = []
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until a request slot is available, then consume it.

        This method is safe to call concurrently from multiple tasks.
        """
        while True:
            async with self._lock:
                now = time.monotonic()
                # Prune timestamps older than 60 seconds
                self._timestamps = [t for t in self._timestamps if now - t < 60.0]

                # Check per-second window
                recent_1s = sum(1 for t in self._timestamps if now - t < 1.0)
                # Check per-minute window
                recent_60s = len(self._timestamps)

                if recent_1s < self._max_per_second and recent_60s < self._max_per_minute:
                    self._timestamps.append(now)
                    return

            # Back off briefly before retrying
            await asyncio.sleep(0.05)
