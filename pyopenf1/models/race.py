"""Pydantic V2 models for race endpoints: ``/race_control``, ``/pit``, ``/stints``, ``/overtakes``."""

from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel, ConfigDict, Field


class RaceControl(BaseModel):
    """A race control message from the ``/race_control`` endpoint.

    Attributes:
        category: Message category (Flag, SafetyCar, SessionStatus, etc.).
        date: Timestamp of the message.
        driver_number: Related driver number, if applicable.
        flag: Flag type (GREEN, YELLOW, etc.), if applicable.
        lap_number: Related lap number, if applicable.
        meeting_key: Unique meeting key.
        message: Full text of the race control message.
        qualifying_phase: Qualifying phase, if applicable.
        scope: Scope of the message (Track, Driver, Sector).
        sector: Sector number, if applicable.
        session_key: Unique session key.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    category: str = Field(..., description="Message category.")
    date: datetime = Field(..., description="Message timestamp.")
    driver_number: int | None = Field(None, description="Related driver number.")
    flag: str | None = Field(None, description="Flag type.")
    lap_number: int | None = Field(None, description="Related lap number.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    message: str = Field(..., description="Full message text.")
    qualifying_phase: str | None = Field(None, description="Qualifying phase.")
    scope: str | None = Field(None, description="Message scope.")
    sector: int | None = Field(None, description="Sector number.")
    session_key: int = Field(..., description="Unique session key.")


class Pit(BaseModel):
    """Pit stop data from the ``/pit`` endpoint.

    Attributes:
        date: Timestamp of pit entry.
        driver_number: Unique driver number.
        lane_duration: Total time in the pit lane (s).
        lap_number: Lap number of pit entry.
        meeting_key: Unique meeting key.
        pit_duration: Total pit duration (s).
        session_key: Unique session key.
        stop_duration: Stationary stop time (s).
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    date: datetime = Field(..., description="Pit entry timestamp.")
    driver_number: int = Field(..., description="Unique driver number.")
    lane_duration: float | None = Field(None, description="Pit lane duration (s).")
    lap_number: int = Field(..., description="Pit entry lap number.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    pit_duration: float | None = Field(None, description="Total pit duration (s).")
    session_key: int = Field(..., description="Unique session key.")
    stop_duration: float | None = Field(None, description="Stationary stop time (s).")


class Stint(BaseModel):
    """Stint data from the ``/stints`` endpoint.

    Attributes:
        compound: Tyre compound (SOFT, MEDIUM, HARD, etc.).
        driver_number: Unique driver number.
        lap_end: Last lap of the stint.
        lap_start: First lap of the stint.
        meeting_key: Unique meeting key.
        session_key: Unique session key.
        stint_number: Stint number within the session.
        tyre_age_at_start: Tyre age in laps at stint start.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    compound: str = Field(..., description="Tyre compound.")
    driver_number: int = Field(..., description="Unique driver number.")
    lap_end: int | None = Field(None, description="Last lap of stint.")
    lap_start: int = Field(..., description="First lap of stint.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    session_key: int = Field(..., description="Unique session key.")
    stint_number: int = Field(..., description="Stint number.")
    tyre_age_at_start: int = Field(..., description="Tyre age at stint start (laps).")


class Overtake(BaseModel):
    """Overtake data from the ``/overtakes`` endpoint.

    Attributes:
        date: Timestamp of the overtake.
        meeting_key: Unique meeting key.
        overtaken_driver_number: Driver who was overtaken.
        overtaking_driver_number: Driver who overtook.
        position: Position at which the overtake occurred.
        session_key: Unique session key.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    date: datetime = Field(..., description="Overtake timestamp.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    overtaken_driver_number: int = Field(..., description="Overtaken driver.")
    overtaking_driver_number: int = Field(..., description="Overtaking driver.")
    position: int = Field(..., description="Position of overtake.")
    session_key: int = Field(..., description="Unique session key.")
