"""Results endpoint methods for ``/session_result`` and ``/starting_grid``."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter

from pyopenf1.core.http_client import BaseHTTPClient  # noqa: TC001
from pyopenf1.models.results import SessionResult, StartingGrid

_result_adapter: TypeAdapter[list[SessionResult]] = TypeAdapter(list[SessionResult])
_grid_adapter: TypeAdapter[list[StartingGrid]] = TypeAdapter(list[StartingGrid])


class ResultsAPI:
    """High-level interface for results endpoints.

    Args:
        http: A shared :class:`BaseHTTPClient` instance.
    """

    def __init__(self, http: BaseHTTPClient) -> None:
        self._http = http

    async def get_session_results(
        self,
        *,
        session_key: int | None = None,
        driver_number: int | None = None,
        **extra_params: Any,
    ) -> list[SessionResult]:
        """Fetch session results from ``/session_result``."""
        params: dict[str, Any] = {**extra_params}
        if session_key is not None:
            params["session_key"] = session_key
        if driver_number is not None:
            params["driver_number"] = driver_number
        raw: Any = await self._http.request("GET", "/session_result", params=params)
        return _result_adapter.validate_python(raw)

    async def get_starting_grid(
        self, *, session_key: int | None = None, **extra_params: Any
    ) -> list[StartingGrid]:
        """Fetch starting grid from ``/starting_grid``."""
        params: dict[str, Any] = {**extra_params}
        if session_key is not None:
            params["session_key"] = session_key
        raw: Any = await self._http.request("GET", "/starting_grid", params=params)
        return _grid_adapter.validate_python(raw)
