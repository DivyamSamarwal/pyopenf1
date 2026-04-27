#!/usr/bin/env python3
"""Quickstart example for pyopenf1 (async).

Demonstrates fetching data from multiple endpoints using the
``AsyncOpenF1Client``.
"""

from __future__ import annotations

import asyncio

from pyopenf1 import AsyncOpenF1Client, PyOpenF1Error


async def main() -> None:
    """Fetch and display data from multiple OpenF1 endpoints."""
    async with AsyncOpenF1Client() as client:
        try:
            # Fetch car telemetry
            car_data = await client.telemetry.get_car_data(
                driver_number=1, session_key=9159,
            )
            print(f"📡 {len(car_data)} telemetry samples")
            for entry in car_data[:3]:
                print(f"  Speed: {entry.speed} km/h | Gear: {entry.n_gear} | RPM: {entry.rpm}")

            print()

            # Fetch driver info
            drivers = await client.drivers.get_drivers(session_key=9158)
            print(f"🏎️  {len(drivers)} drivers found")
            for d in drivers[:5]:
                print(f"  #{d.driver_number} {d.full_name} ({d.team_name})")

            print()

            # Fetch weather
            weather = await client.weather.get_weather(meeting_key=1219)
            if weather:
                w = weather[0]
                print(f"🌡️  Air: {w.air_temperature}°C | Track: {w.track_temperature}°C")

        except PyOpenF1Error as exc:
            print(f"❌ API error: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
