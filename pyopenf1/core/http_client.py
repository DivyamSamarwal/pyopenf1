"""Low-level HTTP transport layer wrapping :class:`httpx.AsyncClient`.

This module is the single point of contact with the network.  All endpoint
classes delegate their HTTP calls through :class:`BaseHTTPClient`, which
handles:

* Base URL resolution and default headers
* Connection pooling and timeout configuration
* Automatic retry with exponential backoff (via ``tenacity``)
* Client-side rate limiting (via :class:`~pyopenf1.core.rate_limiter.RateLimiter`)
* Optional response caching (via :class:`~pyopenf1.core.cache.TTLCache`)
* Structured logging
* Automatic mapping of HTTP error codes to typed exceptions
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

if TYPE_CHECKING:
    from pyopenf1.core.cache import TTLCache
from pyopenf1.core.rate_limiter import RateLimiter
from pyopenf1.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
)

logger = logging.getLogger("pyopenf1")

_DEFAULT_BASE_URL = "https://api.openf1.org/v1"
_DEFAULT_TIMEOUT = 30.0
_DEFAULT_MAX_CONNECTIONS = 100
_DEFAULT_MAX_KEEPALIVE = 20


class BaseHTTPClient:
    """Async HTTP client wrapper tuned for the OpenF1 API.

    This class owns the ``httpx.AsyncClient`` lifecycle and exposes a
    thin ``request`` helper that:

    * resolves paths relative to the OpenF1 base URL,
    * injects default headers (``Accept: application/json``),
    * enforces client-side rate limits,
    * caches responses when a cache is configured,
    * retries transient failures with exponential backoff,
    * maps HTTP 4xx / 5xx responses to typed exceptions.

    Args:
        base_url: Root URL of the OpenF1 API.
        timeout: Request timeout in seconds.
        headers: Extra headers merged with the defaults.
        max_retries: Maximum number of retry attempts for transient errors.
        rate_limiter: Optional rate limiter instance.  A default free-tier
            limiter (3 req/s, 30 req/min) is created when ``None``.
        cache: Optional TTL cache instance for response caching.
            Pass ``None`` to disable caching (default).

    Usage::

        async with BaseHTTPClient() as http:
            data = await http.request("GET", "/car_data", params={"driver_number": 1})
    """

    def __init__(
        self,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        headers: dict[str, str] | None = None,
        max_retries: int = 3,
        rate_limiter: RateLimiter | None = None,
        cache: TTLCache | None = None,
    ) -> None:
        default_headers: dict[str, str] = {
            "Accept": "application/json",
            "User-Agent": "pyopenf1/0.1.0",
        }
        if headers:
            default_headers.update(headers)

        pool_limits = httpx.Limits(
            max_connections=_DEFAULT_MAX_CONNECTIONS,
            max_keepalive_connections=_DEFAULT_MAX_KEEPALIVE,
        )

        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers=default_headers,
            timeout=httpx.Timeout(timeout),
            limits=pool_limits,
        )

        self._max_retries = max_retries
        self._rate_limiter = rate_limiter or RateLimiter()
        self._cache = cache

    # ------------------------------------------------------------------
    # Context-manager support
    # ------------------------------------------------------------------

    async def aclose(self) -> None:
        """Gracefully close the underlying HTTP connection pool."""
        await self._client.aclose()
        logger.debug("HTTP client closed.")

    async def __aenter__(self) -> BaseHTTPClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        await self.aclose()

    # ------------------------------------------------------------------
    # Core request helper
    # ------------------------------------------------------------------

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        use_cache: bool = True,
    ) -> Any:
        """Send an HTTP request and return the parsed JSON body.

        Args:
            method: HTTP method (``GET``, ``POST``, etc.).
            path: URL path relative to the base URL (e.g. ``/car_data``).
            params: Optional query-string parameters.
            json: Optional JSON body for ``POST`` / ``PUT`` requests.
            use_cache: Whether to use the cache (if configured).

        Returns:
            The decoded JSON response body (typically a ``list`` or ``dict``).

        Raises:
            RateLimitError: On HTTP 429.
            AuthenticationError: On HTTP 401 / 403.
            NotFoundError: On HTTP 404.
            ServerError: On HTTP 5xx.
            APIError: On any other non-2xx status code.
        """
        # Check cache first
        cache_key = ""
        if self._cache is not None and use_cache and method.upper() == "GET":
            cache_key = self._cache._make_key(method, path, params)
            cached = await self._cache.get(cache_key)
            if cached is not None:
                logger.debug("Cache HIT for %s %s", method, path)
                return cached

        # Acquire rate-limit slot
        await self._rate_limiter.acquire()

        logger.debug("Requesting %s %s params=%s", method, path, params)
        result = await self._request_with_retry(method, path, params=params, json=json)

        # Store in cache
        if self._cache is not None and use_cache and method.upper() == "GET" and cache_key:
            await self._cache.set(cache_key, result)

        return result

    async def _request_with_retry(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Execute the request with tenacity retry logic.

        Retries on :class:`RateLimitError` and :class:`ServerError`
        with exponential backoff.
        """

        @retry(
            stop=stop_after_attempt(self._max_retries),
            wait=wait_exponential(multiplier=1, min=1, max=30),
            retry=retry_if_exception_type((RateLimitError, ServerError)),
            reraise=True,
        )
        async def _do_request() -> Any:
            response = await self._client.request(
                method,
                path,
                params=params,
                json=json,
            )

            if response.is_success:
                logger.debug(
                    "Response %s %s -> %d (%d bytes)",
                    method,
                    path,
                    response.status_code,
                    len(response.content),
                )
                return response.json()

            self._raise_for_status(response)

        return await _do_request()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        """Map an HTTP error response to the appropriate exception type.

        Args:
            response: The ``httpx.Response`` with a non-2xx status code.

        Raises:
            RateLimitError: On HTTP 429.
            AuthenticationError: On HTTP 401 / 403.
            NotFoundError: On HTTP 404.
            ServerError: On HTTP 5xx.
            APIError: On any other non-2xx status code.
        """
        status = response.status_code
        body = response.text

        logger.warning("HTTP error %d for %s %s", status, response.request.method, response.url)

        if status == 429:
            retry_after_raw = response.headers.get("Retry-After")
            retry_after = float(retry_after_raw) if retry_after_raw else None
            raise RateLimitError(
                f"Rate limit exceeded (HTTP {status}).",
                status_code=status,
                response_body=body,
                retry_after=retry_after,
            )

        if status in {401, 403}:
            raise AuthenticationError(
                f"Authentication failed (HTTP {status}).",
                status_code=status,
                response_body=body,
            )

        if status == 404:
            raise NotFoundError(
                f"Resource not found (HTTP {status}).",
                status_code=status,
                response_body=body,
            )

        if 500 <= status < 600:
            raise ServerError(
                f"Server error (HTTP {status}).",
                status_code=status,
                response_body=body,
            )

        raise APIError(
            f"API request failed (HTTP {status}).",
            status_code=status,
            response_body=body,
        )
