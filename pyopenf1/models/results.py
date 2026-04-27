"""Pydantic V2 models for ``/session_result`` and ``/starting_grid`` endpoints."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SessionResult(BaseModel):
    """Post-session result from the ``/session_result`` endpoint.

    Attributes:
        dnf: Did not finish.
        dns: Did not start.
        dsq: Disqualified.
        driver_number: Unique driver number.
        duration: Fastest lap / race duration in seconds.
        gap_to_leader: Gap to leader in seconds or laps.
        number_of_laps: Number of laps completed.
        meeting_key: Unique meeting key.
        position: Final position.
        session_key: Unique session key.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    dnf: bool = Field(False, description="Did not finish.")
    dns: bool = Field(False, description="Did not start.")
    dsq: bool = Field(False, description="Disqualified.")
    driver_number: int = Field(..., description="Unique driver number.")
    duration: float | None = Field(None, description="Duration in seconds.")
    gap_to_leader: float | str | None = Field(None, description="Gap to leader.")
    number_of_laps: int | None = Field(None, description="Laps completed.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    position: int = Field(..., description="Final position.")
    session_key: int = Field(..., description="Unique session key.")


class StartingGrid(BaseModel):
    """Starting grid position from the ``/starting_grid`` endpoint.

    Attributes:
        driver_number: Unique driver number.
        lap_duration: Qualifying lap duration in seconds.
        meeting_key: Unique meeting key.
        position: Grid position.
        session_key: Unique session key.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    driver_number: int = Field(..., description="Unique driver number.")
    lap_duration: float | None = Field(None, description="Qualifying lap (s).")
    meeting_key: int = Field(..., description="Unique meeting key.")
    position: int = Field(..., description="Grid position.")
    session_key: int = Field(..., description="Unique session key.")
