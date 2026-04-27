"""Pydantic V2 model for the ``/drivers`` endpoint."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Driver(BaseModel):
    """Detailed information about a driver in a specific session.

    Attributes:
        broadcast_name: Broadcast-style name (e.g. "M VERSTAPPEN").
        driver_number: Unique driver number.
        first_name: Driver's first name.
        full_name: Full name (e.g. "Max VERSTAPPEN").
        headshot_url: URL to driver's headshot image.
        last_name: Driver's last name.
        meeting_key: Unique meeting key.
        name_acronym: Three-letter acronym (e.g. "VER").
        session_key: Unique session key.
        team_colour: Hex colour code of the team (without #).
        team_name: Full team name.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    broadcast_name: str = Field(..., description="Broadcast-style name.")
    driver_number: int = Field(..., description="Unique driver number.")
    first_name: str = Field(..., description="First name.")
    full_name: str = Field(..., description="Full name.")
    headshot_url: str | None = Field(None, description="URL to headshot image.")
    last_name: str = Field(..., description="Last name.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    name_acronym: str = Field(..., description="Three-letter acronym.")
    session_key: int = Field(..., description="Unique session key.")
    team_colour: str | None = Field(None, description="Hex team colour.")
    team_name: str = Field(..., description="Full team name.")
