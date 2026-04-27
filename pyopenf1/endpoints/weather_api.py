"""Weather endpoint methods."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter

from pyopenf1.core.http_client import BaseHTTPClient  # noqa: TC001
from pyopenf1.models.weather import Weather

_weather_adapter: TypeAdapter[list[Weather]] = TypeAdapter(list[Weather])


class WeatherAPI:
    """High-level interface for ``/weather``.

    Args:
        http: A shared :class:`BaseHTTPClient` instance.
    """

    def __init__(self, http: BaseHTTPClient) -> None:
        self._http = http

    async def get_weather(
        self, *, session_key: int | None = None, meeting_key: int | None = None, **extra_params: Any
    ) -> list[Weather]:
        """Fetch weather data from ``/weather``."""
        params: dict[str, Any] = {**extra_params}
        if session_key is not None:
            params["session_key"] = session_key
        if meeting_key is not None:
            params["meeting_key"] = meeting_key
        raw: Any = await self._http.request("GET", "/weather", params=params)
        return _weather_adapter.validate_python(raw)
