# 🏎️ pyopenf1

A production-grade, asynchronous Python wrapper for the [OpenF1 API](https://openf1.org).

## Features

- **Fully Async** — Built on `httpx.AsyncClient` with first-class `async/await` support
- **Synchronous Wrapper** — `OpenF1Client` for non-async usage
- **All 18 Endpoints** — Complete coverage of the OpenF1 API
- **Pydantic V2 Models** — Validated, typed responses
- **Auto-Retry** — Exponential backoff on 429/5xx errors
- **Rate Limiting** — Client-side throttling to prevent 429s
- **Response Caching** — Optional TTL cache for immutable data
- **CLI Tool** — `pyopenf1 car-data --driver 1`
- **DataFrame Support** — Optional pandas integration

## Installation

```bash
pip install pyopenf1
```

With pandas support:

```bash
pip install pyopenf1[pandas]
```

## Quick Example

```python
import asyncio
from pyopenf1 import AsyncOpenF1Client

async def main():
    async with AsyncOpenF1Client() as client:
        data = await client.telemetry.get_car_data(driver_number=1, session_key=9159)
        for entry in data[:5]:
            print(f"Speed: {entry.speed} km/h")

asyncio.run(main())
```
