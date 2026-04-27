"""Pydantic V2 model for the ``/team_radio`` endpoint."""

from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel, ConfigDict, Field


class TeamRadio(BaseModel):
    """A team radio communication from the ``/team_radio`` endpoint.

    Attributes:
        date: Timestamp of the radio message.
        driver_number: Unique driver number.
        meeting_key: Unique meeting key.
        recording_url: URL to the MP3 recording.
        session_key: Unique session key.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    date: datetime = Field(..., description="Radio message timestamp.")
    driver_number: int = Field(..., description="Unique driver number.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    recording_url: str = Field(..., description="URL to MP3 recording.")
    session_key: int = Field(..., description="Unique session key.")
