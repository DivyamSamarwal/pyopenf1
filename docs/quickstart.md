# Quickstart

This guide will walk you through initializing the `pyopenf1` client and making your first requests to the OpenF1 API.

## 1. Choose Your Client

`pyopenf1` provides two clients. Both use the exact same methods and return the exact same Pydantic models.

*   `AsyncOpenF1Client`: The primary, high-performance async client.
*   `OpenF1Client`: A synchronous wrapper for simple scripts or Jupyter Notebooks.

=== "AsyncOpenF1Client"
    ```python
    import asyncio
    from pyopenf1 import AsyncOpenF1Client

    async def main():
        async with AsyncOpenF1Client() as client:
            drivers = await client.drivers.get_drivers(session_key=9158)
            print(f"Loaded {len(drivers)} drivers.")

    asyncio.run(main())
    ```

=== "OpenF1Client (Sync)"
    ```python
    from pyopenf1 import OpenF1Client

    with OpenF1Client() as client:
        drivers = client.drivers.get_drivers(session_key=9158)
        print(f"Loaded {len(drivers)} drivers.")
    ```

> [!NOTE]
> **Why `async with`?** 
> The client utilizes underlying connection pools (via `httpx`). Using the `with` or `async with` context manager ensures that connections are properly closed and memory is freed when your script finishes. If you don't use the context manager, you must manually call `client.close()`.

---

## 2. Fetching Telemetry Data

The OpenF1 API is massive. Let's fetch some high-frequency car telemetry data!

```python
async with AsyncOpenF1Client() as client:
    # 1. Fetch the telemetry array
    data = await client.telemetry.get_car_data(driver_number=1, session_key=9159)
    
    # 2. Iterate through the parsed Pydantic objects
    for entry in data[5000:5005]:
        print(f"Time: {entry.date} | Speed: {entry.speed} km/h | Gear: {entry.n_gear}")
```

> [!WARNING]
> Because cars sit stationary in the garage for a long time before a session starts, if you print `data[:5]` (the very beginning of the array), the speed and gear will be `0`.

---

## 3. Endpoints Overview

The client organizes the OpenF1 API into intuitive namespaces:

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

*Next Steps: Check out the [Pandas Integration](pandas.md) or [Advanced Usage](advanced.md) guides!*
