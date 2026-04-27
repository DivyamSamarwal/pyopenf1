#!/usr/bin/env python3
"""Synchronous client example for pyopenf1.

Demonstrates how to use the sync ``OpenF1Client`` without async/await.
"""

from __future__ import annotations

from pyopenf1 import OpenF1Client, PyOpenF1Error


def main() -> None:
    """Fetch driver and session info synchronously."""
    with OpenF1Client() as client:
        try:
            drivers = client.drivers.get_drivers(session_key=9158)
            print(f"Found {len(drivers)} drivers\n")
            for d in drivers[:5]:
                print(f"  #{d.driver_number} {d.full_name} - {d.team_name}")

        except PyOpenF1Error as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
