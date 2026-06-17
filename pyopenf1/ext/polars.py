"""Optional polars DataFrame integration.

Convert any list of Pydantic models returned by pyopenf1 into a
polars DataFrame with a single call.

Requires ``polars`` to be installed::

    pip install pyopenf1[polars]
"""

from __future__ import annotations

from typing import Any


def to_polars(models: list[Any]) -> Any:
    """Convert a list of Pydantic models to a polars DataFrame.

    Args:
        models: A list of Pydantic BaseModel instances (e.g. from
            ``client.telemetry.get_car_data(...)``).

    Returns:
        A ``polars.DataFrame`` with one row per model.

    Raises:
        ImportError: If ``polars`` is not installed.
        ValueError: If the input list is empty.

    Example::

        from pyopenf1.ext.polars import to_polars

        data = await client.telemetry.get_car_data(driver_number=1)
        df = to_polars(data)
        print(df.head())
    """
    try:
        import polars as pl
    except ImportError as exc:
        raise ImportError(
            "polars is required for DataFrame conversion. "
            "Install it with: pip install pyopenf1[polars]"
        ) from exc

    if not models:
        return pl.DataFrame()

    rows = [m.model_dump() for m in models]
    return pl.DataFrame(rows)
