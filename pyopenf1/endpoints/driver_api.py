"""Driver endpoint methods."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter

from pyopenf1.core.http_client import BaseHTTPClient  # noqa: TC001
from pyopenf1.models.driver import Driver

_driver_adapter: TypeAdapter[list[Driver]] = TypeAdapter(list[Driver])


class DriverAPI:
    """High-level interface for ``/drivers``.

    Args:
        http: A shared :class:`BaseHTTPClient` instance.
    """

    def __init__(self, http: BaseHTTPClient) -> None:
        self._http = http

    async def get_drivers(
        self,
        *,
        driver_number: int | None = None,
        session_key: int | None = None,
        name_acronym: str | None = None,
        team_name: str | None = None,
        **extra_params: Any,
    ) -> list[Driver]:
        """Fetch driver information from ``/drivers``.

        Args:
            driver_number: Filter by driver number.
            session_key: Filter by session key.
            name_acronym: Filter by three-letter acronym (e.g. "VER").
            team_name: Filter by team name.
            **extra_params: Additional query filters.

        Returns:
            A list of :class:`Driver` models.
        """
        params: dict[str, Any] = {**extra_params}
        if driver_number is not None:
            params["driver_number"] = driver_number
        if session_key is not None:
            params["session_key"] = session_key
        if name_acronym is not None:
            params["name_acronym"] = name_acronym
        if team_name is not None:
            params["team_name"] = team_name

        raw: Any = await self._http.request("GET", "/drivers", params=params)
        return _driver_adapter.validate_python(raw)
