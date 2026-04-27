"""Team radio endpoint methods."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter

from pyopenf1.core.http_client import BaseHTTPClient  # noqa: TC001
from pyopenf1.models.team_radio import TeamRadio

_radio_adapter: TypeAdapter[list[TeamRadio]] = TypeAdapter(list[TeamRadio])


class TeamRadioAPI:
    """High-level interface for ``/team_radio``.

    Args:
        http: A shared :class:`BaseHTTPClient` instance.
    """

    def __init__(self, http: BaseHTTPClient) -> None:
        self._http = http

    async def get_team_radio(
        self,
        *,
        session_key: int | None = None,
        driver_number: int | None = None,
        **extra_params: Any,
    ) -> list[TeamRadio]:
        """Fetch team radio communications from ``/team_radio``."""
        params: dict[str, Any] = {**extra_params}
        if session_key is not None:
            params["session_key"] = session_key
        if driver_number is not None:
            params["driver_number"] = driver_number
        raw: Any = await self._http.request("GET", "/team_radio", params=params)
        return _radio_adapter.validate_python(raw)
