"""Timing endpoint methods for ``/laps``, ``/intervals``, ``/position``."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter

from pyopenf1.core.http_client import BaseHTTPClient  # noqa: TC001
from pyopenf1.models.timing import Interval, Lap, Position

_lap_adapter: TypeAdapter[list[Lap]] = TypeAdapter(list[Lap])
_interval_adapter: TypeAdapter[list[Interval]] = TypeAdapter(list[Interval])
_position_adapter: TypeAdapter[list[Position]] = TypeAdapter(list[Position])


class TimingAPI:
    """High-level interface for timing endpoints.

    Args:
        http: A shared :class:`BaseHTTPClient` instance.
    """

    def __init__(self, http: BaseHTTPClient) -> None:
        self._http = http

    async def get_laps(
        self,
        *,
        driver_number: int | None = None,
        session_key: int | None = None,
        lap_number: int | None = None,
        **extra_params: Any,
    ) -> list[Lap]:
        """Fetch lap data from ``/laps``.

        Args:
            driver_number: Filter by driver number.
            session_key: Filter by session key.
            lap_number: Filter by lap number.
            **extra_params: Additional query filters.

        Returns:
            A list of :class:`Lap` models.
        """
        params: dict[str, Any] = {**extra_params}
        if driver_number is not None:
            params["driver_number"] = driver_number
        if session_key is not None:
            params["session_key"] = session_key
        if lap_number is not None:
            params["lap_number"] = lap_number

        raw: Any = await self._http.request("GET", "/laps", params=params)
        return _lap_adapter.validate_python(raw)

    async def get_intervals(
        self,
        *,
        driver_number: int | None = None,
        session_key: int | None = None,
        **extra_params: Any,
    ) -> list[Interval]:
        """Fetch interval data from ``/intervals``.

        Args:
            driver_number: Filter by driver number.
            session_key: Filter by session key.
            **extra_params: Additional query filters.

        Returns:
            A list of :class:`Interval` models.
        """
        params: dict[str, Any] = {**extra_params}
        if driver_number is not None:
            params["driver_number"] = driver_number
        if session_key is not None:
            params["session_key"] = session_key

        raw: Any = await self._http.request("GET", "/intervals", params=params)
        return _interval_adapter.validate_python(raw)

    async def get_positions(
        self,
        *,
        driver_number: int | None = None,
        session_key: int | None = None,
        meeting_key: int | None = None,
        **extra_params: Any,
    ) -> list[Position]:
        """Fetch position data from ``/position``.

        Args:
            driver_number: Filter by driver number.
            session_key: Filter by session key.
            meeting_key: Filter by meeting key.
            **extra_params: Additional query filters.

        Returns:
            A list of :class:`Position` models.
        """
        params: dict[str, Any] = {**extra_params}
        if driver_number is not None:
            params["driver_number"] = driver_number
        if session_key is not None:
            params["session_key"] = session_key
        if meeting_key is not None:
            params["meeting_key"] = meeting_key

        raw: Any = await self._http.request("GET", "/position", params=params)
        return _position_adapter.validate_python(raw)
