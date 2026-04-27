"""Session and meeting endpoint methods."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter

from pyopenf1.core.http_client import BaseHTTPClient  # noqa: TC001
from pyopenf1.models.session import Meeting, Session

_session_adapter: TypeAdapter[list[Session]] = TypeAdapter(list[Session])
_meeting_adapter: TypeAdapter[list[Meeting]] = TypeAdapter(list[Meeting])


class SessionAPI:
    """High-level interface for ``/sessions`` and ``/meetings``.

    Args:
        http: A shared :class:`BaseHTTPClient` instance.
    """

    def __init__(self, http: BaseHTTPClient) -> None:
        self._http = http

    async def get_sessions(
        self,
        *,
        session_key: int | None = None,
        meeting_key: int | None = None,
        session_name: str | None = None,
        country_name: str | None = None,
        year: int | None = None,
        **extra_params: Any,
    ) -> list[Session]:
        """Fetch session data from ``/sessions``.

        Args:
            session_key: Filter by session key.
            meeting_key: Filter by meeting key.
            session_name: Filter by session name.
            country_name: Filter by country.
            year: Filter by year.
            **extra_params: Additional query filters.

        Returns:
            A list of :class:`Session` models.
        """
        params: dict[str, Any] = {**extra_params}
        if session_key is not None:
            params["session_key"] = session_key
        if meeting_key is not None:
            params["meeting_key"] = meeting_key
        if session_name is not None:
            params["session_name"] = session_name
        if country_name is not None:
            params["country_name"] = country_name
        if year is not None:
            params["year"] = year

        raw: Any = await self._http.request("GET", "/sessions", params=params)
        return _session_adapter.validate_python(raw)

    async def get_meetings(
        self,
        *,
        meeting_key: int | None = None,
        country_name: str | None = None,
        year: int | None = None,
        **extra_params: Any,
    ) -> list[Meeting]:
        """Fetch meeting data from ``/meetings``.

        Args:
            meeting_key: Filter by meeting key.
            country_name: Filter by country.
            year: Filter by year.
            **extra_params: Additional query filters.

        Returns:
            A list of :class:`Meeting` models.
        """
        params: dict[str, Any] = {**extra_params}
        if meeting_key is not None:
            params["meeting_key"] = meeting_key
        if country_name is not None:
            params["country_name"] = country_name
        if year is not None:
            params["year"] = year

        raw: Any = await self._http.request("GET", "/meetings", params=params)
        return _meeting_adapter.validate_python(raw)
