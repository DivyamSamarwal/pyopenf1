"""Facade client for the OpenF1 API.

:class:`AsyncOpenF1Client` is the primary entry-point for end-users.  It
owns the HTTP transport and exposes every API domain as a property.

Usage::

    async with AsyncOpenF1Client() as f1:
        data = await f1.telemetry.get_car_data(driver_number=1)
"""

from __future__ import annotations

from typing import Any

from pyopenf1.core.cache import TTLCache
from pyopenf1.core.http_client import BaseHTTPClient
from pyopenf1.core.rate_limiter import RateLimiter
from pyopenf1.endpoints.championship_api import ChampionshipAPI
from pyopenf1.endpoints.driver_api import DriverAPI
from pyopenf1.endpoints.race_api import RaceAPI
from pyopenf1.endpoints.results_api import ResultsAPI
from pyopenf1.endpoints.session_api import SessionAPI
from pyopenf1.endpoints.team_radio_api import TeamRadioAPI
from pyopenf1.endpoints.telemetry_api import TelemetryAPI
from pyopenf1.endpoints.timing_api import TimingAPI
from pyopenf1.endpoints.weather_api import WeatherAPI


class AsyncOpenF1Client:
    """Asynchronous client for interacting with the OpenF1 API.

    This is the main facade that should be used by consumers of the
    library.  It manages the lifecycle of the underlying HTTP connection
    pool and exposes domain-specific API namespaces as properties.

    Args:
        base_url: Override the default OpenF1 API base URL.
        timeout: HTTP request timeout in seconds.
        headers: Extra HTTP headers merged into every request.
        max_retries: Maximum retry attempts for transient errors.
        cache_ttl: TTL in seconds for response cache.  ``0`` disables caching.
        max_per_second: Rate limit: max requests per second.
        max_per_minute: Rate limit: max requests per minute.

    Example::

        async with AsyncOpenF1Client() as client:
            drivers = await client.drivers.get_drivers(session_key=9158)
            for d in drivers:
                print(f"{d.name_acronym} - {d.team_name}")
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
        cache = TTLCache(default_ttl=cache_ttl) if cache_ttl > 0 else None
        rate_limiter = RateLimiter(
            max_per_second=max_per_second,
            max_per_minute=max_per_minute,
        )

        self._http = BaseHTTPClient(
            base_url=base_url,
            timeout=timeout,
            headers=headers,
            max_retries=max_retries,
            rate_limiter=rate_limiter,
            cache=cache,
        )

        # Domain API namespaces
        self._telemetry = TelemetryAPI(self._http)
        self._sessions = SessionAPI(self._http)
        self._drivers = DriverAPI(self._http)
        self._timing = TimingAPI(self._http)
        self._race = RaceAPI(self._http)
        self._championship = ChampionshipAPI(self._http)
        self._results = ResultsAPI(self._http)
        self._weather = WeatherAPI(self._http)
        self._team_radio = TeamRadioAPI(self._http)

    # ------------------------------------------------------------------
    # Public API namespaces
    # ------------------------------------------------------------------

    @property
    def telemetry(self) -> TelemetryAPI:
        """Access telemetry / car-data / location endpoints."""
        return self._telemetry

    @property
    def sessions(self) -> SessionAPI:
        """Access session and meeting endpoints."""
        return self._sessions

    @property
    def drivers(self) -> DriverAPI:
        """Access driver information endpoints."""
        return self._drivers

    @property
    def timing(self) -> TimingAPI:
        """Access lap, interval, and position endpoints."""
        return self._timing

    @property
    def race(self) -> RaceAPI:
        """Access race control, pit, stint, and overtake endpoints."""
        return self._race

    @property
    def championship(self) -> ChampionshipAPI:
        """Access championship standings endpoints."""
        return self._championship

    @property
    def results(self) -> ResultsAPI:
        """Access session result and starting grid endpoints."""
        return self._results

    @property
    def weather(self) -> WeatherAPI:
        """Access weather endpoints."""
        return self._weather

    @property
    def team_radio(self) -> TeamRadioAPI:
        """Access team radio endpoints."""
        return self._team_radio

    # ------------------------------------------------------------------
    # Context-manager protocol
    # ------------------------------------------------------------------

    async def aclose(self) -> None:
        """Close the underlying HTTP client and release resources."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncOpenF1Client:
        """Enter the async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit the async context manager, closing the HTTP pool."""
        await self.aclose()
