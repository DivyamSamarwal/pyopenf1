"""Pydantic V2 models for the OpenF1 telemetry endpoints.

Covers ``/car_data`` and ``/location`` endpoints.
"""

from __future__ import annotations

from datetime import datetime  # noqa: TC003 — required at runtime by Pydantic

from pydantic import BaseModel, ConfigDict, Field


class CarData(BaseModel):
    """A single telemetry sample from the ``/car_data`` endpoint.

    Each record represents a snapshot of a car's live telemetry at a
    specific timestamp during a session.

    Attributes:
        brake: Brake application percentage (0-100).
        date: ISO-8601 timestamp of the telemetry sample.
        driver_number: The unique number identifying the driver.
        drs: DRS (Drag Reduction System) status code.
        meeting_key: Unique key identifying the meeting (Grand Prix).
        n_gear: Current gear number (0 = neutral).
        rpm: Engine revolutions per minute.
        session_key: The unique key identifying the session.
        speed: Car speed in km/h.
        throttle: Throttle position percentage (0-100).
    """

    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    brake: int = Field(..., ge=0, le=100, description="Brake percentage.")
    date: datetime = Field(..., description="ISO-8601 timestamp of the sample.")
    driver_number: int = Field(..., description="Unique driver number.")
    drs: int = Field(..., description="DRS status flag.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    n_gear: int = Field(..., ge=0, le=8, description="Current gear (0 = neutral).")
    rpm: int = Field(..., ge=0, description="Engine RPM.")
    session_key: int = Field(..., description="Unique session key.")
    speed: int = Field(..., ge=0, description="Car speed in km/h.")
    throttle: int = Field(..., ge=0, le=100, description="Throttle percentage.")


class Location(BaseModel):
    """A single GPS location sample from the ``/location`` endpoint.

    Provides the approximate position of a car on the circuit at ~3.7 Hz.

    Attributes:
        date: ISO-8601 timestamp of the location sample.
        driver_number: Unique driver number.
        meeting_key: Unique meeting key.
        session_key: Unique session key.
        x: X coordinate on the circuit.
        y: Y coordinate on the circuit.
        z: Z coordinate (elevation).
    """

    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    date: datetime = Field(..., description="ISO-8601 timestamp.")
    driver_number: int = Field(..., description="Unique driver number.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    session_key: int = Field(..., description="Unique session key.")
    x: int = Field(..., description="X coordinate on the circuit.")
    y: int = Field(..., description="Y coordinate on the circuit.")
    z: int = Field(..., description="Z coordinate (elevation).")
