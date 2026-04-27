"""pyopenf1 --- Async Python wrapper for the OpenF1 API.

Usage::

    import asyncio
    from pyopenf1 import AsyncOpenF1Client

    async def main() -> None:
        async with AsyncOpenF1Client() as client:
            car_data = await client.telemetry.get_car_data(driver_number=1)
            print(car_data)

    asyncio.run(main())
"""

from pyopenf1.client import AsyncOpenF1Client
from pyopenf1.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    PyOpenF1Error,
    RateLimitError,
    ServerError,
)
from pyopenf1.sync_client import OpenF1Client

__all__ = [
    "APIError",
    "AsyncOpenF1Client",
    "AuthenticationError",
    "NotFoundError",
    "OpenF1Client",
    "PyOpenF1Error",
    "RateLimitError",
    "ServerError",
]

__version__ = "0.1.0"
