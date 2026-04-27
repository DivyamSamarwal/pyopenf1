<p align="center">
  <h1 align="center">🏎️ pyopenf1</h1>
  <p align="center">
    A production-grade, asynchronous Python wrapper for the <a href="https://openf1.org">OpenF1 API</a>.
  </p>
  <p align="center">
    <a href="https://pypi.org/project/pyopenf1/"><img src="https://img.shields.io/pypi/v/pyopenf1?color=blue&label=PyPI" alt="PyPI"></a>
    <a href="https://github.com/divya/pyopenf1/actions"><img src="https://img.shields.io/github/actions/workflow/status/divya/pyopenf1/ci.yml?branch=main&label=CI" alt="CI"></a>
    <a href="https://pypi.org/project/pyopenf1/"><img src="https://img.shields.io/pypi/pyversions/pyopenf1" alt="Python versions"></a>
    <a href="https://github.com/divya/pyopenf1/blob/main/LICENSE"><img src="https://img.shields.io/github/license/divya/pyopenf1" alt="License"></a>
  </p>
</p>

---

## ✨ Features

- **Fully Async** — Built on `httpx.AsyncClient` with first-class `async/await` support.
- **Sync Wrapper** — `OpenF1Client` for users who don't need async.
- **All 18 Endpoints** — Complete coverage: telemetry, laps, drivers, sessions, weather, pit stops, stints, overtakes, race control, team radio, championship standings, results, starting grid, and more.
- **Pydantic V2 Models** — Every response is validated and returned as a strict, typed model.
- **Auto-Retry** — Exponential backoff on 429/5xx via `tenacity`.
- **Rate Limiting** — Built-in client-side throttle (3 req/s free tier).
- **Response Caching** — Optional in-memory TTL cache.
- **CLI Tool** — Query the API from your terminal.
- **DataFrame Support** — Optional `pandas` integration.
- **Production-Ready** — Custom exceptions, structured logging, connection pooling.

## 📦 Installation

```bash
pip install pyopenf1
```

With pandas support:
```bash
pip install pyopenf1[pandas]
```

## 🚀 Quickstart

### Async (recommended)

```python
import asyncio
from pyopenf1 import AsyncOpenF1Client

async def main() -> None:
    async with AsyncOpenF1Client() as client:
        # Fetch telemetry
        car_data = await client.telemetry.get_car_data(driver_number=1, session_key=9159)
        for entry in car_data[:5]:
            print(f"Speed: {entry.speed} km/h | Gear: {entry.n_gear}")

        # Fetch drivers
        drivers = await client.drivers.get_drivers(session_key=9158)
        for d in drivers[:3]:
            print(f"#{d.driver_number} {d.full_name} - {d.team_name}")

asyncio.run(main())
```

### Sync

```python
from pyopenf1 import OpenF1Client

with OpenF1Client() as client:
    drivers = client.drivers.get_drivers(session_key=9158)
    for d in drivers:
        print(f"{d.name_acronym} - {d.team_name}")
```

### CLI

```bash
pyopenf1 car-data --driver 1 --session 9159 --format table
pyopenf1 drivers --session 9158 --format json
pyopenf1 weather --meeting 1208 --format csv --output weather.csv
```

### DataFrame

```python
from pyopenf1.ext.pandas import to_dataframe

data = await client.telemetry.get_car_data(driver_number=1)
df = to_dataframe(data)
print(df.describe())
```

## ⚙️ Configuration

```python
async with AsyncOpenF1Client(
    cache_ttl=300.0,        # Cache responses for 5 minutes
    max_retries=5,          # Retry up to 5 times
    max_per_second=6.0,     # Sponsor-tier rate limit
    max_per_minute=60.0,
) as client:
    ...
```

## 📡 Available Endpoints

| Namespace | Methods | OpenF1 Endpoints |
|-----------|---------|------------------|
| `client.telemetry` | `get_car_data()`, `get_location()` | `/car_data`, `/location` |
| `client.sessions` | `get_sessions()`, `get_meetings()` | `/sessions`, `/meetings` |
| `client.drivers` | `get_drivers()` | `/drivers` |
| `client.timing` | `get_laps()`, `get_intervals()`, `get_positions()` | `/laps`, `/intervals`, `/position` |
| `client.race` | `get_race_control()`, `get_pit_stops()`, `get_stints()`, `get_overtakes()` | `/race_control`, `/pit`, `/stints`, `/overtakes` |
| `client.championship` | `get_drivers_championship()`, `get_teams_championship()` | `/championship_drivers`, `/championship_teams` |
| `client.results` | `get_session_results()`, `get_starting_grid()` | `/session_result`, `/starting_grid` |
| `client.weather` | `get_weather()` | `/weather` |
| `client.team_radio` | `get_team_radio()` | `/team_radio` |

## 🏗️ Architecture

```
pyopenf1/
├── __init__.py              # Public API surface
├── client.py                # AsyncOpenF1Client facade
├── sync_client.py           # OpenF1Client (sync wrapper)
├── cli.py                   # Click CLI
├── exceptions.py            # Custom exception hierarchy
├── core/
│   ├── http_client.py       # httpx wrapper + retry + logging
│   ├── rate_limiter.py      # Token-bucket rate limiter
│   └── cache.py             # In-memory TTL cache
├── models/                  # Pydantic V2 data models
│   ├── telemetry.py         # CarData, Location
│   ├── session.py           # Session, Meeting
│   ├── driver.py            # Driver
│   ├── timing.py            # Lap, Interval, Position
│   ├── race.py              # RaceControl, Pit, Stint, Overtake
│   ├── championship.py      # ChampionshipDriver, ChampionshipTeam
│   ├── results.py           # SessionResult, StartingGrid
│   ├── weather.py           # Weather
│   └── team_radio.py        # TeamRadio
├── endpoints/               # API endpoint classes
│   ├── telemetry_api.py
│   ├── session_api.py
│   ├── driver_api.py
│   ├── timing_api.py
│   ├── race_api.py
│   ├── championship_api.py
│   ├── results_api.py
│   ├── weather_api.py
│   └── team_radio_api.py
└── ext/
    └── pandas.py            # Optional DataFrame integration
```

## 🧪 Development

```bash
# Install dev dependencies
poetry install

# Lint & format
poetry run ruff check .
poetry run ruff format .

# Type check
poetry run mypy pyopenf1/

# Test
poetry run pytest -v

# Build docs
poetry run mkdocs serve
```

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
