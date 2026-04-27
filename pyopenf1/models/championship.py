"""Pydantic V2 models for championship endpoints."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ChampionshipDriver(BaseModel):
    """Driver championship standing from ``/championship_drivers``.

    Attributes:
        driver_number: Unique driver number.
        meeting_key: Unique meeting key.
        points_current: Current points tally.
        points_start: Points before this meeting.
        position_current: Current championship position.
        position_start: Position before this meeting.
        session_key: Unique session key.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    driver_number: int = Field(..., description="Unique driver number.")
    meeting_key: int = Field(..., description="Unique meeting key.")
    points_current: float = Field(..., description="Current points.")
    points_start: float = Field(..., description="Points before meeting.")
    position_current: int = Field(..., description="Current position.")
    position_start: int = Field(..., description="Position before meeting.")
    session_key: int = Field(..., description="Unique session key.")


class ChampionshipTeam(BaseModel):
    """Team championship standing from ``/championship_teams``.

    Attributes:
        meeting_key: Unique meeting key.
        points_current: Current points tally.
        points_start: Points before this meeting.
        position_current: Current championship position.
        position_start: Position before this meeting.
        session_key: Unique session key.
        team_name: Full team name.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, str_strip_whitespace=True)

    meeting_key: int = Field(..., description="Unique meeting key.")
    points_current: float = Field(..., description="Current points.")
    points_start: float = Field(..., description="Points before meeting.")
    position_current: int = Field(..., description="Current position.")
    position_start: int = Field(..., description="Position before meeting.")
    session_key: int = Field(..., description="Unique session key.")
    team_name: str = Field(..., description="Full team name.")
