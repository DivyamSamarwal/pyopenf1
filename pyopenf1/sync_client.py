"""Synchronous wrapper for the OpenF1 API.

Provides :class:`OpenF1Client` for users who do not want to use
``async/await``.  Every method mirrors :class:`AsyncOpenF1Client`
but runs synchronously.
"""

from __future__ import annotations

import asyncio
from typing import Any

from pyopenf1.client import AsyncOpenF1Client


class OpenF1Client:
    """Synchronous client for the OpenF1 API.

    Wraps :class:`AsyncOpenF1Client` and runs all coroutines in an
    event loop.  Supports standard ``with`` context manager.

    Args:
        base_url: Override the default OpenF1 API base URL.
        timeout: HTTP request timeout in seconds.
        headers: Extra HTTP headers.
        max_retries: Maximum retry attempts for transient errors.
        cache_ttl: TTL in seconds for response cache.  ``0`` disables.
        max_per_second: Rate limit: max requests per second.
        max_per_minute: Rate limit: max requests per minute.

    Example::

        with OpenF1Client() as client:
            drivers = client.drivers.get_drivers(session_key=9158)
            for d in drivers:
                print(d.full_name)
    """

    def __init__(
        self,
        *,
        base_url: str = "https://api.openf1.org/v1",
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
        max_retries: int = 3,
        cache_ttl: float = 0.0,
        max_per_second: float = 3.0,
        max_per_minute: float = 30.0,
    ) -> None:
        self._async_client = AsyncOpenF1Client(
            base_url=base_url,
            timeout=timeout,
            headers=headers,
            max_retries=max_retries,
            cache_ttl=cache_ttl,
            max_per_second=max_per_second,
            max_per_minute=max_per_minute,
        )
        self._loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

    def _get_loop(self) -> asyncio.AbstractEventLoop:
        """Get or re-create the event loop if it has been closed."""
        if self._loop.is_closed():
            self._loop = asyncio.new_event_loop()
        return self._loop

    def _run(self, coro: Any) -> Any:
        """Run an async coroutine synchronously."""
        return self._get_loop().run_until_complete(coro)

    @property
    def telemetry(self) -> _SyncNamespace:
        """Access telemetry endpoints synchronously."""
        return _SyncNamespace(self._async_client.telemetry, self._run)

    @property
    def sessions(self) -> _SyncNamespace:
        """Access session endpoints synchronously."""
        return _SyncNamespace(self._async_client.sessions, self._run)

    @property
    def drivers(self) -> _SyncNamespace:
        """Access driver endpoints synchronously."""
        return _SyncNamespace(self._async_client.drivers, self._run)

    @property
    def timing(self) -> _SyncNamespace:
        """Access timing endpoints synchronously."""
        return _SyncNamespace(self._async_client.timing, self._run)

    @property
    def race(self) -> _SyncNamespace:
        """Access race endpoints synchronously."""
        return _SyncNamespace(self._async_client.race, self._run)

    @property
    def championship(self) -> _SyncNamespace:
        """Access championship endpoints synchronously."""
        return _SyncNamespace(self._async_client.championship, self._run)

    @property
    def results(self) -> _SyncNamespace:
        """Access results endpoints synchronously."""
        return _SyncNamespace(self._async_client.results, self._run)

    @property
    def weather(self) -> _SyncNamespace:
        """Access weather endpoints synchronously."""
        return _SyncNamespace(self._async_client.weather, self._run)

    @property
    def team_radio(self) -> _SyncNamespace:
        """Access team radio endpoints synchronously."""
        return _SyncNamespace(self._async_client.team_radio, self._run)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._run(self._async_client.aclose())
        if self._loop and not self._loop.is_closed():
            self._loop.close()

    def __enter__(self) -> OpenF1Client:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        self.close()


class _SyncNamespace:
    """Wraps an async API namespace to make methods callable synchronously.

    Uses ``__getattr__`` to intercept method calls and run them
    through the event loop.
    """

    def __init__(self, async_ns: Any, runner: Any) -> None:
        self._async_ns = async_ns
        self._runner = runner

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._async_ns, name)
        if callable(attr):

            def sync_method(*args: Any, **kwargs: Any) -> Any:
                return self._runner(attr(*args, **kwargs))

            return sync_method
        return attr
