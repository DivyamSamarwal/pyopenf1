# Data Science (Pandas)

If you are performing data analysis, plotting telemetry with `matplotlib`, or training machine learning models, raw Python lists of Pydantic objects can be slow and cumbersome.

`pyopenf1` includes a built-in extension to instantly flatten these payloads into high-performance `pandas` DataFrames.

## Installation

Ensure you have the pandas extra installed:

```bash
pip install "pyopenf1[pandas]"
```

## Creating DataFrames

Use the `to_dataframe()` utility function to convert any list of OpenF1 models into a DataFrame.

```python
import asyncio
from pyopenf1 import AsyncOpenF1Client
from pyopenf1.ext.pandas import to_dataframe

async def analyze_telemetry():
    async with AsyncOpenF1Client() as client:
        # 1. Fetch raw Pydantic models
        raw_data = await client.telemetry.get_car_data(driver_number=1, session_key=9159)
        
        # 2. Convert to DataFrame
        df = to_dataframe(raw_data)
        
        # 3. Analyze!
        print(df.describe())
        print(f"Max Speed: {df['speed'].max()} km/h")

asyncio.run(analyze_telemetry())
```

> [!TIP]
> `to_dataframe` automatically handles the timezone-aware `datetime` objects parsed by Pydantic, ensuring your DataFrame indices and time-series plots work flawlessly out of the box!
