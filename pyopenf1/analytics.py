"""High-level analytics helpers for pyopenf1."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyopenf1.client import AsyncOpenF1Client
    from pyopenf1.models.timing import Lap


class Analytics:
    """High-level analytics helpers built on top of the API client.

    Args:
        client: An instance of :class:`AsyncOpenF1Client`.
    """

    def __init__(self, client: AsyncOpenF1Client) -> None:
        self.client = client

    async def get_fastest_lap(self, session_key: int, driver_number: int | None = None) -> Lap | None:
        """Find the fastest lap in a session.

        If ``driver_number`` is provided, finds the fastest lap for that specific driver.
        Otherwise, finds the fastest lap of the entire session.

        Args:
            session_key: The unique session identifier.
            driver_number: Optional driver number to filter by.

        Returns:
            The :class:`Lap` object with the lowest lap duration, or ``None`` if no laps are found.
        """
        laps = await self.client.timing.get_laps(
            session_key=session_key,
            driver_number=driver_number,
        )

        valid_laps = [lap for lap in laps if lap.lap_duration is not None]
        if not valid_laps:
            return None

        return min(valid_laps, key=lambda lap: lap.lap_duration or 0.0)

    async def get_pit_strategy(self, session_key: int) -> dict[int, list[dict[str, Any]]]:
        """Get the pit stop strategy for all drivers in a session.

        Returns a dictionary mapping driver numbers to a list of their pit stops and stints.

        Args:
            session_key: The unique session identifier.

        Returns:
            A dictionary where the key is the driver number and the value is a list of
            stint/pit details.
        """
        stints = await self.client.race.get_stints(session_key=session_key)

        strategy: dict[int, list[dict[str, Any]]] = {}

        for stint in sorted(stints, key=lambda s: s.stint_number):
            if stint.driver_number not in strategy:
                strategy[stint.driver_number] = []

            strategy[stint.driver_number].append({
                "stint_number": stint.stint_number,
                "compound": stint.compound,
                "tyre_age_at_start": stint.tyre_age_at_start,
                "laps": stint.lap_end - stint.lap_start + 1 if stint.lap_end and stint.lap_start else None,
            })

        return strategy
