"""Championship endpoint methods."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter

from pyopenf1.core.http_client import BaseHTTPClient  # noqa: TC001
from pyopenf1.models.championship import ChampionshipDriver, ChampionshipTeam

_champ_driver_adapter: TypeAdapter[list[ChampionshipDriver]] = TypeAdapter(
    list[ChampionshipDriver]
)
_champ_team_adapter: TypeAdapter[list[ChampionshipTeam]] = TypeAdapter(list[ChampionshipTeam])


class ChampionshipAPI:
    """High-level interface for championship endpoints.

    Args:
        http: A shared :class:`BaseHTTPClient` instance.
    """

    def __init__(self, http: BaseHTTPClient) -> None:
        self._http = http

    async def get_drivers_championship(
        self,
        *,
        session_key: int | None = None,
        driver_number: int | None = None,
        **extra_params: Any,
    ) -> list[ChampionshipDriver]:
        """Fetch driver championship standings from ``/championship_drivers``."""
        params: dict[str, Any] = {**extra_params}
        if session_key is not None:
            params["session_key"] = session_key
        if driver_number is not None:
            params["driver_number"] = driver_number
        raw: Any = await self._http.request("GET", "/championship_drivers", params=params)
        return _champ_driver_adapter.validate_python(raw)

    async def get_teams_championship(
        self, *, session_key: int | None = None, team_name: str | None = None, **extra_params: Any
    ) -> list[ChampionshipTeam]:
        """Fetch team championship standings from ``/championship_teams``."""
        params: dict[str, Any] = {**extra_params}
        if session_key is not None:
            params["session_key"] = session_key
        if team_name is not None:
            params["team_name"] = team_name
        raw: Any = await self._http.request("GET", "/championship_teams", params=params)
        return _champ_team_adapter.validate_python(raw)
