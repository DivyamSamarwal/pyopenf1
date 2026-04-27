"""Pydantic V2 models for ``/sessions`` and ``/meetings`` endpoints."""

from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel, ConfigDict, Field


class Session(BaseModel):
    """A Formula 1 session (practice, qualifying, sprint, race, etc.).

    Attributes:
        circuit_key: Unique circuit identifier.
        circuit_short_name: Short name of the circuit.
        country_code: ISO 3-letter country code.
        country_key: Unique country identifier.
        country_name: Full country name.
        date_end: Session end timestamp.
        date_start: Session start timestamp.
        gmt_offset: GMT offset string (e.g. "02:00:00").
        is_cancelled: Whether the session was cancelled.
        location: Circuit location name.
        meeting_key: Unique meeting key.
        session_key: Unique session key.
        session_name: Human-readable session name.
        session_type: Session type (Practice, Qualifying, Race, etc.).
        year: Season year.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    circuit_key: int = Field(..., description="Unique circuit identifier.")
    circuit_short_name: str = Field(..., description="Short circuit name.")
    country_code: str = Field(..., description="ISO 3-letter country code.")
    country_key: int = Field(..., description="Unique country identifier.")
    country_name: str = Field(..., description="Full country name.")
    date_end: datetime = Field(..., description="Session end timestamp.")
    date_start: datetime = Field(..., description="Session start timestamp.")
    gmt_offset: str = Field(..., description="GMT offset string.")
    is_cancelled: bool = Field(False, description="Whether session was cancelled.")
    location: str = Field(..., description="Circuit location name.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    session_key: int = Field(..., description="Unique session key.")
    session_name: str = Field(..., description="Session name.")
    session_type: str = Field(..., description="Session type.")
    year: int = Field(..., description="Season year.")


class Meeting(BaseModel):
    """A Formula 1 meeting (Grand Prix or testing weekend).

    Attributes:
        circuit_key: Unique circuit identifier.
        circuit_short_name: Short circuit name.
        country_code: ISO 3-letter country code.
        country_key: Unique country identifier.
        country_name: Full country name.
        date_end: Meeting end timestamp.
        date_start: Meeting start timestamp.
        gmt_offset: GMT offset string.
        is_cancelled: Whether the meeting was cancelled.
        location: Circuit location name.
        meeting_key: Unique meeting key.
        meeting_name: Human-readable meeting name.
        meeting_official_name: Official FIA meeting name.
        year: Season year.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    circuit_key: int = Field(..., description="Unique circuit identifier.")
    circuit_short_name: str = Field(..., description="Short circuit name.")
    country_code: str = Field(..., description="ISO 3-letter country code.")
    country_key: int = Field(..., description="Unique country identifier.")
    country_name: str = Field(..., description="Full country name.")
    date_end: datetime = Field(..., description="Meeting end timestamp.")
    date_start: datetime = Field(..., description="Meeting start timestamp.")
    gmt_offset: str = Field(..., description="GMT offset string.")
    is_cancelled: bool = Field(False, description="Whether meeting was cancelled.")
    location: str = Field(..., description="Circuit location name.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    meeting_name: str = Field(..., description="Meeting name.")
    meeting_official_name: str = Field(..., description="Official FIA name.")
    year: int = Field(..., description="Season year.")
