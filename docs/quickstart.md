# Quickstart

## Async Client

```python
import asyncio
from pyopenf1 import AsyncOpenF1Client

async def main():
    async with AsyncOpenF1Client() as client:
        # Telemetry
        car_data = await client.telemetry.get_car_data(driver_number=1, session_key=9159)

        # Drivers
        drivers = await client.drivers.get_drivers(session_key=9158)

        # Weather
        weather = await client.weather.get_weather(meeting_key=1208)

        # Laps
        laps = await client.timing.get_laps(driver_number=63, session_key=9161)

asyncio.run(main())
```

## Sync Client

```python
from pyopenf1 import OpenF1Client

with OpenF1Client() as client:
    drivers = client.drivers.get_drivers(session_key=9158)
    for d in drivers:
        print(f"{d.name_acronym} - {d.team_name}")
```

## Configuration

```python
async with AsyncOpenF1Client(
    cache_ttl=300.0,        # Cache responses for 5 minutes
    max_retries=5,          # Retry up to 5 times on errors
    max_per_second=6.0,     # Sponsor-tier rate limit
    max_per_minute=60.0,
) as client:
    ...
```

## DataFrame Integration

```python
from pyopenf1.ext.pandas import to_dataframe

data = await client.telemetry.get_car_data(driver_number=1)
df = to_dataframe(data)
print(df.describe())
```

## Available Endpoints

| Namespace | Methods |
|-----------|---------|
| `client.telemetry` | `get_car_data()`, `get_location()` |
| `client.sessions` | `get_sessions()`, `get_meetings()` |
| `client.drivers` | `get_drivers()` |
| `client.timing` | `get_laps()`, `get_intervals()`, `get_positions()` |
| `client.race` | `get_race_control()`, `get_pit_stops()`, `get_stints()`, `get_overtakes()` |
| `client.championship` | `get_drivers_championship()`, `get_teams_championship()` |
| `client.results` | `get_session_results()`, `get_starting_grid()` |
| `client.weather` | `get_weather()` |
| `client.team_radio` | `get_team_radio()` |
