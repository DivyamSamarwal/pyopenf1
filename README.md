<div align="center">
  <img src="https://raw.githubusercontent.com/DivyamSamarwal/pyopenf1/main/assets/logo.png" alt="pyopenf1 Logo" width="200" onerror="this.style.display='none'">

  # 🏎️ pyopenf1

  **A production-grade, asynchronous Python wrapper for the [OpenF1 API](https://openf1.org).**

  [![PyPI - Version](https://img.shields.io/pypi/v/pyopenf1?style=for-the-badge&color=blue)](https://pypi.org/project/pyopenf1/)
  [![PyPI - Downloads](https://img.shields.io/pypi/dm/pyopenf1?style=for-the-badge&color=green)](https://pypi.org/project/pyopenf1/)
  [![Python Versions](https://img.shields.io/pypi/pyversions/pyopenf1?style=for-the-badge)](https://pypi.org/project/pyopenf1/)
  [![CI Status](https://img.shields.io/github/actions/workflow/status/DivyamSamarwal/pyopenf1/ci.yml?branch=main&style=for-the-badge&label=CI)](https://github.com/DivyamSamarwal/pyopenf1/actions)
  [![License](https://img.shields.io/github/license/DivyamSamarwal/pyopenf1?style=for-the-badge)](https://github.com/DivyamSamarwal/pyopenf1/blob/main/LICENSE)

  <br />

  *[Read the Documentation](https://github.com/DivyamSamarwal/pyopenf1#readme) • [Report a Bug](https://github.com/DivyamSamarwal/pyopenf1/issues)*
</div>

<hr />

## ✨ Why `pyopenf1`?

`pyopenf1` is designed for performance, reliability, and developer experience. Whether you're building a real-time race dashboard, training machine learning models on telemetry, or just having fun with F1 data, this library gives you everything you need.

> 📊 **First-Class Data Integration**: Convert raw telemetry into Pandas or Polars DataFrames with a single method call.
>
> 🚀 **Built for Speed**: Fully asynchronous, connection pooling, and in-memory TTL caching.
> 
> 🛡️ **Production Ready**: Pydantic V2 validation, exponential backoff retries, and strict rate-limiting built-in.

---

## ⚡ Features Overview

- **100% API Coverage**: All 18 OpenF1 endpoints supported natively.
- **Async & Sync Support**: Use `AsyncOpenF1Client` for high-throughput, or `OpenF1Client` for simple scripts.
- **Pydantic V2 Models**: Every response is strictly validated and strongly typed.
- **Interactive TUI Dashboard**: Launch a live terminal UI with `pyopenf1 dashboard`.
- **Advanced Analytics**: Pre-built helpers for calculating fastest laps and extracting pit strategies.
- **Data Science Ready**: Native `pandas` and `polars` integration.
- **Resilient**: Smart retries and token-bucket rate limiting to prevent `429 Too Many Requests`.

---

## 📦 Installation

Install the base package via `pip` or `poetry`:

```bash
pip install pyopenf1
```

### 🔋 Supercharge with Extras
Depending on your use-case, you can install optional dependencies for enhanced functionality:

```bash
pip install "pyopenf1[pandas]"   # Export data to Pandas DataFrames
pip install "pyopenf1[polars]"   # Export data to blazing-fast Polars DataFrames
pip install "pyopenf1[tui]"      # Unlock the interactive terminal dashboard
pip install "pyopenf1[all]"      # Install everything!
```

---

## 🚀 Quickstart

### The Async Way (Recommended)
Unleash the full power of concurrent HTTP requests:

```python
import asyncio
from pyopenf1 import AsyncOpenF1Client

async def main():
    async with AsyncOpenF1Client() as client:
        # Fetch high-frequency telemetry data
        car_data = await client.telemetry.get_car_data(driver_number=1, session_key=9159)
        
        print(f"Loaded {len(car_data)} telemetry frames!")
        for entry in car_data[:5]:
            print(f"Speed: {entry.speed} km/h | Gear: {entry.n_gear} | RPM: {entry.rpm}")

asyncio.run(main())
```

### The Sync Way
Perfect for quick scripts or Jupyter notebooks:

```python
from pyopenf1 import OpenF1Client

with OpenF1Client() as client:
    drivers = client.drivers.get_drivers(session_key=9158)
    for driver in drivers:
        print(f"{driver.name_acronym} - {driver.team_name} (Car {driver.driver_number})")
```

---

## 📊 Data Science & Analytics

### Polars & Pandas Integration
Stop writing boilerplate conversion code. `pyopenf1` does it for you:

```python
from pyopenf1.ext.polars import to_polars
from pyopenf1.ext.pandas import to_dataframe

# Fetch Pydantic models
data = await client.telemetry.get_car_data(driver_number=1)

# Convert to Polars
df_pl = to_polars(data)

# Convert to Pandas
df_pd = to_dataframe(data)
```

### High-Level Analytics
Let `pyopenf1` do the heavy lifting for complex race analysis:

```python
from pyopenf1.analytics import Analytics

analytics = Analytics(client)

# Find the fastest lap of the session
fastest = await analytics.get_fastest_lap(session_key=9158)
print(f"Fastest lap: {fastest.lap_duration} seconds")

# Get pit stop strategies for the whole grid
strategies = await analytics.get_pit_strategy(session_key=9158)
```

---

## 🖥️ CLI & Terminal Dashboard

You don't even need to write code to use `pyopenf1`! 

### The TUI Dashboard
Launch a beautiful, interactive terminal dashboard to view session data live:
```bash
pyopenf1 dashboard --session 9158
```
*(Note: Requires the `[tui]` extra)*

### Command-Line Interface
Query the API and export directly to CSV/JSON right from your terminal:
```bash
# Get weather data and save as CSV
pyopenf1 weather --meeting 1208 --format csv --output weather.csv

# Fetch driver info as pretty JSON
pyopenf1 drivers --session 9158 --format json
```

---

## ⚙️ Advanced Configuration

Fine-tune your client for aggressive caching and optimized rate limits:

```python
async with AsyncOpenF1Client(
    cache_ttl=300.0,        # Cache responses for 5 minutes
    max_retries=5,          # Retry up to 5 times on server errors
    max_per_second=6.0,     # Perfect for sponsor-tier API limits
    max_per_minute=60.0,
) as client:
    ...
```

---

## 📡 Available Endpoints Directory

| Domain | Methods | OpenF1 Endpoints |
|-----------|---------|------------------|
| **Telemetry** | `get_car_data()`, `get_location()` | `/car_data`, `/location` |
| **Sessions** | `get_sessions()`, `get_meetings()` | `/sessions`, `/meetings` |
| **Drivers** | `get_drivers()` | `/drivers` |
| **Timing** | `get_laps()`, `get_intervals()`, `get_positions()` | `/laps`, `/intervals`, `/position` |
| **Race** | `get_race_control()`, `get_pit_stops()`, `get_stints()`, `get_overtakes()` | `/race_control`, `/pit`, `/stints`, `/overtakes` |
| **Championship** | `get_drivers_championship()`, `get_teams_championship()` | `/championship_drivers`, `/championship_teams` |
| **Results** | `get_session_results()`, `get_starting_grid()` | `/session_result`, `/starting_grid` |
| **Weather** | `get_weather()` | `/weather` |
| **Radio** | `get_team_radio()` | `/team_radio` |

---

## 🤝 Contributing & Development

We welcome contributions! To get started:

```bash
# Install dependencies using Poetry
poetry install --all-extras

# Run the test suite
poetry run pytest -v

# Run the linter & formatter
poetry run ruff check .
poetry run ruff format .
```

---

## 📄 License

This project is distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more details.

<div align="center">
  <br/>
  <i>Built with ❤️ for F1 Data Enthusiasts</i>
</div>
