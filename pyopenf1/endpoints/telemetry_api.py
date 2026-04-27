"""Telemetry endpoint methods for ``/car_data`` and ``/location``."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter

from pyopenf1.core.http_client import BaseHTTPClient  # noqa: TC001
from pyopenf1.models.telemetry import CarData, Location

_car_data_adapter: TypeAdapter[list[CarData]] = TypeAdapter(list[CarData])
_location_adapter: TypeAdapter[list[Location]] = TypeAdapter(list[Location])


class TelemetryAPI:
    """High-level interface for telemetry queries.

    Args:
        http: A shared :class:`BaseHTTPClient` instance.
    """

    def __init__(self, http: BaseHTTPClient) -> None:
        self._http = http

    async def get_car_data(
        self,
        *,
        driver_number: int | None = None,
        session_key: int | None = None,
        speed_gte: int | None = None,
        **extra_params: Any,
    ) -> list[CarData]:
        """Fetch car telemetry data from ``/car_data``.

        Args:
            driver_number: Filter by driver number.
            session_key: Filter by session key.
            speed_gte: Filter for speed >= value.
            **extra_params: Additional query filters.

        Returns:
            A list of :class:`CarData` models.
        """
        params: dict[str, Any] = {**extra_params}
        if driver_number is not None:
            params["driver_number"] = driver_number
        if session_key is not None:
            params["session_key"] = session_key
        if speed_gte is not None:
            params["speed>="] = speed_gte

        raw: Any = await self._http.request("GET", "/car_data", params=params)
        return _car_data_adapter.validate_python(raw)

    async def get_location(
        self,
        *,
        driver_number: int | None = None,
        session_key: int | None = None,
        **extra_params: Any,
    ) -> list[Location]:
        """Fetch car location data from ``/location``.

        Args:
            driver_number: Filter by driver number.
            session_key: Filter by session key.
            **extra_params: Additional query filters.

        Returns:
            A list of :class:`Location` models.
        """
        params: dict[str, Any] = {**extra_params}
        if driver_number is not None:
            params["driver_number"] = driver_number
        if session_key is not None:
            params["session_key"] = session_key

        raw: Any = await self._http.request("GET", "/location", params=params)
        return _location_adapter.validate_python(raw)
