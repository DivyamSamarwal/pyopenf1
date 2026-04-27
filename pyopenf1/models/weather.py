"""Pydantic V2 model for the ``/weather`` endpoint."""

from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel, ConfigDict, Field


class Weather(BaseModel):
    """Track weather data from the ``/weather`` endpoint.

    Updated approximately every minute.

    Attributes:
        air_temperature: Air temperature in Celsius.
        date: Timestamp of the weather reading.
        humidity: Relative humidity percentage.
        meeting_key: Unique meeting key.
        pressure: Atmospheric pressure in hPa.
        rainfall: Rainfall indicator (0 = dry).
        session_key: Unique session key.
        track_temperature: Track surface temperature in Celsius.
        wind_direction: Wind direction in degrees.
        wind_speed: Wind speed in m/s.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    air_temperature: float = Field(..., description="Air temperature (C).")
    date: datetime = Field(..., description="Weather reading timestamp.")
    humidity: float = Field(..., description="Relative humidity (%).")
    meeting_key: int = Field(..., description="Unique meeting key.")
    pressure: float = Field(..., description="Atmospheric pressure (hPa).")
    rainfall: int = Field(..., description="Rainfall indicator.")
    session_key: int = Field(..., description="Unique session key.")
    track_temperature: float = Field(..., description="Track temperature (C).")
    wind_direction: int = Field(..., description="Wind direction (degrees).")
    wind_speed: float = Field(..., description="Wind speed (m/s).")
