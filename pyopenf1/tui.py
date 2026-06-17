"""Terminal User Interface dashboard using Textual."""

from __future__ import annotations

from typing import ClassVar

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header, Label

from pyopenf1.client import AsyncOpenF1Client


class DashboardApp(App[None]):
    """A Textual TUI for viewing OpenF1 data.

    Currently supports viewing driver standings for a specific session.
    """

    TITLE = "🏎️ pyopenf1 Dashboard"
    BINDINGS: ClassVar[list[tuple[str, str, str]]] = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, session_key: int | None = None) -> None:
        super().__init__()
        self.session_key = session_key or 9158  # Default to a known session if none provided

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Label(f"Session Key: {self.session_key}", id="session-info")
        yield DataTable(id="drivers-table")
        yield Footer()

    async def on_mount(self) -> None:
        """Fetch data and populate the table when the app starts."""
        table = self.query_one(DataTable)
        table.add_columns("Number", "Name", "Team", "Acronym")

        async with AsyncOpenF1Client() as client:
            try:
                drivers = await client.drivers.get_drivers(session_key=self.session_key)
                for driver in drivers:
                    table.add_row(
                        str(driver.driver_number),
                        driver.full_name,
                        driver.team_name,
                        driver.name_acronym,
                    )
            except Exception as e:
                table.add_row("Error", str(e), "", "")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


def run_dashboard(session_key: int | None = None) -> None:
    """Run the TUI dashboard."""
    app = DashboardApp(session_key=session_key)
    app.run()
