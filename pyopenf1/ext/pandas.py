"""Optional pandas DataFrame integration.

Convert any list of Pydantic models returned by pyopenf1 into a
pandas DataFrame with a single call.

Requires ``pandas`` to be installed::

    pip install pyopenf1[pandas]
"""

from __future__ import annotations

from typing import Any


def to_dataframe(models: list[Any]) -> Any:
    """Convert a list of Pydantic models to a pandas DataFrame.

    Args:
        models: A list of Pydantic BaseModel instances (e.g. from
            ``client.telemetry.get_car_data(...)``).

    Returns:
        A ``pandas.DataFrame`` with one row per model.

    Raises:
        ImportError: If ``pandas`` is not installed.
        ValueError: If the input list is empty.

    Example::

        from pyopenf1.ext.pandas import to_dataframe

        data = await client.telemetry.get_car_data(driver_number=1)
        df = to_dataframe(data)
        print(df.head())
    """
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "pandas is required for DataFrame conversion. "
            "Install it with: pip install pyopenf1[pandas]"
        ) from exc

    if not models:
        return pd.DataFrame()

    rows = [m.model_dump(mode="json") for m in models]
    return pd.DataFrame(rows)
