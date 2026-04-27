"""Race endpoint methods for ``/race_control``, ``/pit``, ``/stints``, ``/overtakes``."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter

from pyopenf1.core.http_client import BaseHTTPClient  # noqa: TC001
from pyopenf1.models.race import Overtake, Pit, RaceControl, Stint

_race_control_adapter: TypeAdapter[list[RaceControl]] = TypeAdapter(list[RaceControl])
_pit_adapter: TypeAdapter[list[Pit]] = TypeAdapter(list[Pit])
_stint_adapter: TypeAdapter[list[Stint]] = TypeAdapter(list[Stint])
_overtake_adapter: TypeAdapter[list[Overtake]] = TypeAdapter(list[Overtake])


class RaceAPI:
    """High-level interface for race-related endpoints.

    Args:
        http: A shared :class:`BaseHTTPClient` instance.
    """

    def __init__(self, http: BaseHTTPClient) -> None:
        self._http = http

    async def get_race_control(
        self, *, session_key: int | None = None, flag: str | None = None, **extra_params: Any
    ) -> list[RaceControl]:
        """Fetch race control messages from ``/race_control``."""
        params: dict[str, Any] = {**extra_params}
        if session_key is not None:
            params["session_key"] = session_key
        if flag is not None:
            params["flag"] = flag
        raw: Any = await self._http.request("GET", "/race_control", params=params)
        return _race_control_adapter.validate_python(raw)

    async def get_pit_stops(
        self,
        *,
        session_key: int | None = None,
        driver_number: int | None = None,
        **extra_params: Any,
    ) -> list[Pit]:
        """Fetch pit stop data from ``/pit``."""
        params: dict[str, Any] = {**extra_params}
        if session_key is not None:
            params["session_key"] = session_key
        if driver_number is not None:
            params["driver_number"] = driver_number
        raw: Any = await self._http.request("GET", "/pit", params=params)
        return _pit_adapter.validate_python(raw)

    async def get_stints(
        self,
        *,
        session_key: int | None = None,
        driver_number: int | None = None,
        **extra_params: Any,
    ) -> list[Stint]:
        """Fetch stint data from ``/stints``."""
        params: dict[str, Any] = {**extra_params}
        if session_key is not None:
            params["session_key"] = session_key
        if driver_number is not None:
            params["driver_number"] = driver_number
        raw: Any = await self._http.request("GET", "/stints", params=params)
        return _stint_adapter.validate_python(raw)

    async def get_overtakes(
        self, *, session_key: int | None = None, **extra_params: Any
    ) -> list[Overtake]:
        """Fetch overtake data from ``/overtakes``."""
        params: dict[str, Any] = {**extra_params}
        if session_key is not None:
            params["session_key"] = session_key
        raw: Any = await self._http.request("GET", "/overtakes", params=params)
        return _overtake_adapter.validate_python(raw)
