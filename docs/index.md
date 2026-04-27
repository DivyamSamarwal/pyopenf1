# 🏎️ pyopenf1

A production-grade, asynchronous Python wrapper for the [OpenF1 API](https://openf1.org).

---

## ⚡ Features

<div class="grid cards" markdown>

-   :material-clock-fast: **Fully Async**
    <hr>
    Built from the ground up on `httpx.AsyncClient` with first-class `async/await` support for high-concurrency scraping.

-   :material-code-json: **Pydantic V2 Validated**
    <hr>
    Every JSON response is rigidly typed and parsed into immutable Pydantic V2 Data Models. Say goodbye to `KeyError`.

-   :material-shield-check: **Bulletproof Rate Limiter**
    <hr>
    Includes a client-side Token Bucket rate limiter that preemptively prevents `429 Too Many Requests` bans before they happen.

-   :material-cached: **Auto-Retry & TTL Cache**
    <hr>
    Exponential backoff on 5xx errors via `tenacity`, combined with an optional in-memory TTL Cache for historical data.

-   :material-table-large: **Pandas Ready**
    <hr>
    Includes an optional `pyopenf1.ext.pandas` extension to instantly flatten nested Pydantic arrays into DataFrames.

-   :material-console: **Rich CLI Tool**
    <hr>
    Extract data directly from your terminal into JSON, CSV, or formatted Tables without writing a single line of Python.

</div>

---

## 📦 Installation

Install via pip:

```bash
pip install pyopenf1
```

> [!TIP]
> If you are a Data Scientist or Analyst and want to use the DataFrame integration, install the pandas extra:
> ```bash
> pip install "pyopenf1[pandas]"
> ```

---

## 🚦 Quick Peek

=== "Async (High Performance)"
    ```python
    import asyncio
    from pyopenf1 import AsyncOpenF1Client

    async def main():
        async with AsyncOpenF1Client() as client:
            # Fetch Max Verstappen's telemetry!
            data = await client.telemetry.get_car_data(driver_number=1, session_key=9159)
            
            for entry in data[5000:5005]:
                print(f"Speed: {entry.speed} km/h | Gear: {entry.n_gear}")

    asyncio.run(main())
    ```

=== "Sync (Simple scripts)"
    ```python
    from pyopenf1 import OpenF1Client

    with OpenF1Client() as client:
        # Fetch Max Verstappen's telemetry!
        data = client.telemetry.get_car_data(driver_number=1, session_key=9159)
        
        for entry in data[5000:5005]:
            print(f"Speed: {entry.speed} km/h | Gear: {entry.n_gear}")
    ```

[Get Started ->](quickstart.md){ .md-button .md-button--primary }
