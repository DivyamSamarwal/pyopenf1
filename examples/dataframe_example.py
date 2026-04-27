#!/usr/bin/env python3
"""DataFrame integration example for pyopenf1.

Requires: pip install pyopenf1[pandas]
"""

from __future__ import annotations

import asyncio

from pyopenf1 import AsyncOpenF1Client
from pyopenf1.ext.pandas import to_dataframe


async def main() -> None:
    """Fetch telemetry and convert to a pandas DataFrame."""
    async with AsyncOpenF1Client() as client:
        car_data = await client.telemetry.get_car_data(
            driver_number=55, session_key=9159,
        )

        if not car_data:
            print("No data found.")
            return

        df = to_dataframe(car_data)
        print(f"DataFrame shape: {df.shape}")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\n{df.head(10)}")
        print(f"\nSpeed stats:\n{df['speed'].describe()}")


if __name__ == "__main__":
    asyncio.run(main())
