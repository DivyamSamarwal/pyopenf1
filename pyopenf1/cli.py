"""CLI interface for pyopenf1.

Usage::

    pyopenf1 car-data --driver 1 --session 9159
    pyopenf1 drivers --session 9158
    pyopenf1 weather --meeting 1208 --format table
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

import click

from pyopenf1.client import AsyncOpenF1Client


def _run(coro: Any) -> Any:
    """Run an async coroutine synchronously."""
    return asyncio.run(coro)


def _output(data: list[Any], fmt: str, output_file: str | None) -> None:
    """Format and output results.

    Args:
        data: List of Pydantic models.
        fmt: Output format ('json', 'table', 'csv').
        output_file: Optional file path to write to.
    """
    if not data:
        click.echo("No results found.")
        return

    rows = [m.model_dump(mode="json") for m in data]

    if fmt == "json":
        text = json.dumps(rows, indent=2, default=str)
    elif fmt == "csv":
        import csv
        import io

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        text = buf.getvalue()
    else:  # table
        if not rows:
            text = ""
        else:
            headers = list(rows[0].keys())
            col_widths = {h: len(h) for h in headers}
            for row in rows:
                for h in headers:
                    col_widths[h] = max(col_widths[h], len(str(row.get(h, ""))))

            header_line = "  ".join(h.ljust(col_widths[h]) for h in headers)
            separator = "  ".join("-" * col_widths[h] for h in headers)
            lines = [header_line, separator]
            for row in rows[:50]:  # Limit table to 50 rows
                lines.append("  ".join(str(row.get(h, "")).ljust(col_widths[h]) for h in headers))
            if len(rows) > 50:
                lines.append(f"... and {len(rows) - 50} more rows")
            text = "\n".join(lines)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        click.echo(f"Output written to {output_file}")
    else:
        click.echo(text)


@click.group()
@click.version_option(package_name="pyopenf1")
def cli() -> None:
    """pyopenf1 -- CLI for the OpenF1 Formula 1 API."""


@cli.command(name="car-data")
@click.option("--driver", type=int, default=None, help="Driver number.")
@click.option("--session", type=int, default=None, help="Session key.")
@click.option("--format", "fmt", type=click.Choice(["json", "table", "csv"]), default="table")
@click.option("--output", "output_file", type=str, default=None, help="Output file path.")
def car_data(driver: int | None, session: int | None, fmt: str, output_file: str | None) -> None:
    """Fetch car telemetry data."""

    async def _fetch() -> list[Any]:
        async with AsyncOpenF1Client() as client:
            return await client.telemetry.get_car_data(driver_number=driver, session_key=session)

    _output(_run(_fetch()), fmt, output_file)


@cli.command()
@click.option("--driver", type=int, default=None, help="Driver number.")
@click.option("--session", type=int, default=None, help="Session key.")
@click.option("--format", "fmt", type=click.Choice(["json", "table", "csv"]), default="table")
@click.option("--output", "output_file", type=str, default=None, help="Output file path.")
def drivers(driver: int | None, session: int | None, fmt: str, output_file: str | None) -> None:
    """Fetch driver information."""

    async def _fetch() -> list[Any]:
        async with AsyncOpenF1Client() as client:
            return await client.drivers.get_drivers(driver_number=driver, session_key=session)

    _output(_run(_fetch()), fmt, output_file)


@cli.command()
@click.option("--session", type=int, default=None, help="Session key.")
@click.option("--country", type=str, default=None, help="Country name.")
@click.option("--year", type=int, default=None, help="Season year.")
@click.option("--format", "fmt", type=click.Choice(["json", "table", "csv"]), default="table")
@click.option("--output", "output_file", type=str, default=None, help="Output file path.")
def sessions(
    session: int | None,
    country: str | None,
    year: int | None,
    fmt: str,
    output_file: str | None,
) -> None:
    """Fetch session information."""

    async def _fetch() -> list[Any]:
        async with AsyncOpenF1Client() as client:
            return await client.sessions.get_sessions(
                session_key=session, country_name=country, year=year
            )

    _output(_run(_fetch()), fmt, output_file)


@cli.command()
@click.option("--driver", type=int, default=None, help="Driver number.")
@click.option("--session", type=int, default=None, help="Session key.")
@click.option("--lap", type=int, default=None, help="Lap number.")
@click.option("--format", "fmt", type=click.Choice(["json", "table", "csv"]), default="table")
@click.option("--output", "output_file", type=str, default=None, help="Output file path.")
def laps(
    driver: int | None,
    session: int | None,
    lap: int | None,
    fmt: str,
    output_file: str | None,
) -> None:
    """Fetch lap data."""

    async def _fetch() -> list[Any]:
        async with AsyncOpenF1Client() as client:
            return await client.timing.get_laps(
                driver_number=driver, session_key=session, lap_number=lap
            )

    _output(_run(_fetch()), fmt, output_file)


@cli.command()
@click.option("--session", type=int, default=None, help="Session key.")
@click.option("--meeting", type=int, default=None, help="Meeting key.")
@click.option("--format", "fmt", type=click.Choice(["json", "table", "csv"]), default="table")
@click.option("--output", "output_file", type=str, default=None, help="Output file path.")
def weather(session: int | None, meeting: int | None, fmt: str, output_file: str | None) -> None:
    """Fetch weather data."""

    async def _fetch() -> list[Any]:
        async with AsyncOpenF1Client() as client:
            return await client.weather.get_weather(session_key=session, meeting_key=meeting)

    _output(_run(_fetch()), fmt, output_file)


@cli.command()
@click.option("--session", type=int, default=None, help="Session key.")
@click.option("--driver", type=int, default=None, help="Driver number.")
@click.option("--format", "fmt", type=click.Choice(["json", "table", "csv"]), default="table")
@click.option("--output", "output_file", type=str, default=None, help="Output file path.")
def stints(driver: int | None, session: int | None, fmt: str, output_file: str | None) -> None:
    """Fetch stint data."""

    async def _fetch() -> list[Any]:
        async with AsyncOpenF1Client() as client:
            return await client.race.get_stints(session_key=session, driver_number=driver)

    _output(_run(_fetch()), fmt, output_file)


@cli.command(name="team-radio")
@click.option("--session", type=int, default=None, help="Session key.")
@click.option("--driver", type=int, default=None, help="Driver number.")
@click.option("--format", "fmt", type=click.Choice(["json", "table", "csv"]), default="table")
@click.option("--output", "output_file", type=str, default=None, help="Output file path.")
def team_radio(driver: int | None, session: int | None, fmt: str, output_file: str | None) -> None:
    """Fetch team radio communications."""

    async def _fetch() -> list[Any]:
        async with AsyncOpenF1Client() as client:
            return await client.team_radio.get_team_radio(
                session_key=session, driver_number=driver
            )

    _output(_run(_fetch()), fmt, output_file)


if __name__ == "__main__":
    cli()
