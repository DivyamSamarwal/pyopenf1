"""Pydantic V2 models for timing endpoints: ``/laps``, ``/intervals``, ``/position``."""

from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel, ConfigDict, Field


class Lap(BaseModel):
    """Detailed data for a single lap from the ``/laps`` endpoint.

    Attributes:
        date_start: Lap start timestamp.
        driver_number: Unique driver number.
        duration_sector_1: Sector 1 duration in seconds.
        duration_sector_2: Sector 2 duration in seconds.
        duration_sector_3: Sector 3 duration in seconds.
        i1_speed: Speed trap 1 in km/h.
        i2_speed: Speed trap 2 in km/h.
        is_pit_out_lap: Whether this is a pit-out lap.
        lap_duration: Total lap duration in seconds.
        lap_number: Lap number.
        meeting_key: Unique meeting key.
        segments_sector_1: Mini-sector segment values for sector 1.
        segments_sector_2: Mini-sector segment values for sector 2.
        segments_sector_3: Mini-sector segment values for sector 3.
        session_key: Unique session key.
        st_speed: Speed trap speed in km/h.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    date_start: datetime | None = Field(None, description="Lap start timestamp.")
    driver_number: int = Field(..., description="Unique driver number.")
    duration_sector_1: float | None = Field(None, description="Sector 1 duration (s).")
    duration_sector_2: float | None = Field(None, description="Sector 2 duration (s).")
    duration_sector_3: float | None = Field(None, description="Sector 3 duration (s).")
    i1_speed: int | None = Field(None, description="Speed trap 1 (km/h).")
    i2_speed: int | None = Field(None, description="Speed trap 2 (km/h).")
    is_pit_out_lap: bool = Field(False, description="Whether this is a pit-out lap.")
    lap_duration: float | None = Field(None, description="Total lap duration (s).")
    lap_number: int = Field(..., description="Lap number.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    segments_sector_1: list[int] | None = Field(None, description="Sector 1 segments.")
    segments_sector_2: list[int] | None = Field(None, description="Sector 2 segments.")
    segments_sector_3: list[int] | None = Field(None, description="Sector 3 segments.")
    session_key: int = Field(..., description="Unique session key.")
    st_speed: int | None = Field(None, description="Speed trap speed (km/h).")


class Interval(BaseModel):
    """Real-time interval data from the ``/intervals`` endpoint.

    Available during races only, updated approximately every 4 seconds.

    Attributes:
        date: Timestamp of the interval measurement.
        driver_number: Unique driver number.
        gap_to_leader: Gap to the race leader in seconds, or None.
        interval: Interval to the car ahead in seconds, or None.
        meeting_key: Unique meeting key.
        session_key: Unique session key.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    date: datetime = Field(..., description="Interval timestamp.")
    driver_number: int = Field(..., description="Unique driver number.")
    gap_to_leader: float | None = Field(None, description="Gap to leader (s).")
    interval: float | None = Field(None, description="Interval to car ahead (s).")
    meeting_key: int = Field(..., description="Unique meeting key.")
    session_key: int = Field(..., description="Unique session key.")


class Position(BaseModel):
    """Driver position data from the ``/position`` endpoint.

    Attributes:
        date: Timestamp of the position update.
        driver_number: Unique driver number.
        meeting_key: Unique meeting key.
        position: Current position.
        session_key: Unique session key.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    date: datetime = Field(..., description="Position timestamp.")
    driver_number: int = Field(..., description="Unique driver number.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    position: int = Field(..., ge=1, description="Current position.")
    session_key: int = Field(..., description="Unique session key.")
