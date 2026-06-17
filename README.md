<p align="center">
  <h1 align="center">🏎️ pyopenf1</h1>
  <p align="center">
    A production-grade, asynchronous Python wrapper for the <a href="https://openf1.org">OpenF1 API</a>.
  </p>
  <p align="center">
    <a href="https://pypi.org/project/pyopenf1/"><img src="https://img.shields.io/pypi/v/pyopenf1?color=blue&label=PyPI" alt="PyPI"></a>
    <a href="https://pepy.tech/project/pyopenf1"><img src="https://static.pepy.tech/badge/pyopenf1" alt="Downloads"></a>
    <a href="https://github.com/DivyamSamarwal/pyopenf1/actions"><img src="https://img.shields.io/github/actions/workflow/status/DivyamSamarwal/pyopenf1/ci.yml?branch=main&label=CI" alt="CI"></a>
    <a href="https://pypi.org/project/pyopenf1/"><img src="https://img.shields.io/pypi/pyversions/pyopenf1" alt="Python versions"></a>
    <a href="https://github.com/DivyamSamarwal/pyopenf1/blob/main/LICENSE"><img src="https://img.shields.io/github/license/DivyamSamarwal/pyopenf1" alt="License"></a>
  </p>
  
  ![Dashboard Placeholder](/assets/dashboard_placeholder.png)
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
- **Interactive TUI** — A live terminal dashboard (`pyopenf1 dashboard`).
- **DataFrame Support** — Native integration with `pandas` and `polars`.
- **Advanced Analytics** — High-level helpers for fastest laps and pit strategies.
- **CLI Tool** — Query the API from your terminal.
- **Production-Ready** — Custom exceptions, structured logging, connection pooling.

## 📦 Installation

```bash
pip install pyopenf1
```

With optional extras:
```bash
pip install pyopenf1[pandas]   # For pandas DataFrames
pip install pyopenf1[polars]   # For polars DataFrames
pip install pyopenf1[tui]      # For the interactive dashboard
pip install pyopenf1[all]      # To install everything
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

### DataFrames (Pandas & Polars)

```python
from pyopenf1.ext.polars import to_polars
from pyopenf1.ext.pandas import to_dataframe

data = await client.telemetry.get_car_data(driver_number=1)

# To Polars
df_pl = to_polars(data)

# To Pandas
df_pd = to_dataframe(data)
```

### High-Level Analytics

```python
from pyopenf1.analytics import Analytics

async with AsyncOpenF1Client() as client:
    analytics = Analytics(client)
    
    fastest = await analytics.get_fastest_lap(session_key=9158)
    print(fastest.lap_duration)
```

### Jupyter Notebook Cookbooks
Check out the `examples/cookbooks/` directory for interactive tutorials, like plotting track maps with telemetry data!

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
