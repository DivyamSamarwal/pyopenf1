"""Tests for the client facade and telemetry endpoint."""

from __future__ import annotations

from typing import Any, ClassVar

import httpx
import pytest
import respx

from pyopenf1 import APIError, AsyncOpenF1Client, RateLimitError
from pyopenf1.models.telemetry import CarData

MOCK_CAR_DATA = [
    {
        "brake": 0,
        "date": "2023-09-15T13:08:19.923000+00:00",
        "driver_number": 55,
        "drs": 12,
        "meeting_key": 1219,
        "n_gear": 8,
        "rpm": 11141,
        "session_key": 9159,
        "speed": 315,
        "throttle": 99,
    },
    {
        "brake": 100,
        "date": "2023-09-15T13:35:41.808000+00:00",
        "driver_number": 55,
        "drs": 8,
        "meeting_key": 1219,
        "n_gear": 8,
        "rpm": 11023,
        "session_key": 9159,
        "speed": 315,
        "throttle": 57,
    },
]


class TestAsyncOpenF1Client:
    """Test suite for the top-level client facade."""

    @pytest.mark.asyncio
    async def test_client_context_manager(self) -> None:
        """The client can be used as an async context manager."""
        async with AsyncOpenF1Client() as client:
            assert client is not None
            assert client.telemetry is not None
            assert client.sessions is not None
            assert client.drivers is not None
            assert client.timing is not None
            assert client.race is not None
            assert client.championship is not None
            assert client.results is not None
            assert client.weather is not None
            assert client.team_radio is not None

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_car_data_success(self) -> None:
        """A successful /car_data call returns validated CarData models."""
        respx.get(
            "https://api.openf1.org/v1/car_data",
            params={"driver_number": "55", "session_key": "9159"},
        ).mock(return_value=httpx.Response(200, json=MOCK_CAR_DATA))

        async with AsyncOpenF1Client() as client:
            result = await client.telemetry.get_car_data(
                driver_number=55, session_key=9159,
            )

        assert len(result) == 2
        assert all(isinstance(entry, CarData) for entry in result)
        assert result[0].driver_number == 55
        assert result[0].speed == 315
        assert result[0].meeting_key == 1219

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_car_data_empty_response(self) -> None:
        """An empty JSON array yields an empty list."""
        respx.get(
            "https://api.openf1.org/v1/car_data",
            params={"driver_number": "99"},
        ).mock(return_value=httpx.Response(200, json=[]))

        async with AsyncOpenF1Client() as client:
            result = await client.telemetry.get_car_data(driver_number=99)

        assert result == []

    @pytest.mark.asyncio
    @respx.mock
    async def test_rate_limit_raises(self) -> None:
        """HTTP 429 triggers a RateLimitError."""
        respx.get("https://api.openf1.org/v1/car_data").mock(
            return_value=httpx.Response(
                429, json={"detail": "Too many requests"}, headers={"Retry-After": "5"},
            ),
        )

        async with AsyncOpenF1Client(max_retries=1) as client:
            with pytest.raises(RateLimitError) as exc_info:
                await client.telemetry.get_car_data()

            assert exc_info.value.status_code == 429

    @pytest.mark.asyncio
    @respx.mock
    async def test_server_error_raises(self) -> None:
        """HTTP 500 triggers a ServerError (subclass of APIError)."""
        respx.get("https://api.openf1.org/v1/car_data").mock(
            return_value=httpx.Response(500, text="Internal Server Error"),
        )

        async with AsyncOpenF1Client(max_retries=1) as client:
            with pytest.raises(APIError) as exc_info:
                await client.telemetry.get_car_data()

            assert exc_info.value.status_code == 500


class TestDriversEndpoint:
    """Test suite for the drivers endpoint."""

    MOCK_DRIVERS: ClassVar[list[dict[str, Any]]] = [
        {
            "broadcast_name": "M VERSTAPPEN",
            "driver_number": 1,
            "first_name": "Max",
            "full_name": "Max VERSTAPPEN",
            "headshot_url": "https://example.com/max.png",
            "last_name": "Verstappen",
            "meeting_key": 1219,
            "name_acronym": "VER",
            "session_key": 9158,
            "team_colour": "3671C6",
            "team_name": "Red Bull Racing",
        }
    ]

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_drivers(self) -> None:
        """Fetch drivers returns validated Driver models."""
        respx.get(
            "https://api.openf1.org/v1/drivers",
            params={"driver_number": "1", "session_key": "9158"},
        ).mock(return_value=httpx.Response(200, json=self.MOCK_DRIVERS))

        async with AsyncOpenF1Client() as client:
            result = await client.drivers.get_drivers(driver_number=1, session_key=9158)

        assert len(result) == 1
        assert result[0].full_name == "Max VERSTAPPEN"
        assert result[0].team_name == "Red Bull Racing"


class TestSessionsEndpoint:
    """Test suite for the sessions endpoint."""

    MOCK_SESSIONS: ClassVar[list[dict[str, Any]]] = [
        {
            "circuit_key": 7,
            "circuit_short_name": "Spa-Francorchamps",
            "country_code": "BEL",
            "country_key": 16,
            "country_name": "Belgium",
            "date_end": "2023-07-29T15:35:00+00:00",
            "date_start": "2023-07-29T15:05:00+00:00",
            "gmt_offset": "02:00:00",
            "is_cancelled": False,
            "location": "Spa-Francorchamps",
            "meeting_key": 1216,
            "session_key": 9140,
            "session_name": "Sprint Qualifying",
            "session_type": "Sprint Qualifying",
            "year": 2023,
        }
    ]

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_sessions(self) -> None:
        """Fetch sessions returns validated Session models."""
        respx.get(
            "https://api.openf1.org/v1/sessions",
            params={"country_name": "Belgium", "year": "2023"},
        ).mock(return_value=httpx.Response(200, json=self.MOCK_SESSIONS))

        async with AsyncOpenF1Client() as client:
            result = await client.sessions.get_sessions(country_name="Belgium", year=2023)

        assert len(result) == 1
        assert result[0].session_name == "Sprint Qualifying"


class TestWeatherEndpoint:
    """Test suite for the weather endpoint."""

    MOCK_WEATHER: ClassVar[list[dict[str, Any]]] = [
        {
            "air_temperature": 27.8,
            "date": "2023-05-07T18:42:25.233000+00:00",
            "humidity": 58,
            "meeting_key": 1208,
            "pressure": 1018.7,
            "rainfall": 0,
            "session_key": 9078,
            "track_temperature": 52.5,
            "wind_direction": 136,
            "wind_speed": 2.4,
        }
    ]

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_weather(self) -> None:
        """Fetch weather returns validated Weather models."""
        respx.get(
            "https://api.openf1.org/v1/weather",
            params={"meeting_key": "1208"},
        ).mock(return_value=httpx.Response(200, json=self.MOCK_WEATHER))

        async with AsyncOpenF1Client() as client:
            result = await client.weather.get_weather(meeting_key=1208)

        assert len(result) == 1
        assert result[0].air_temperature == 27.8
        assert result[0].track_temperature == 52.5


class TestTimingEndpoint:
    """Test suite for timing endpoints."""

    MOCK_LAPS: ClassVar[list[dict[str, Any]]] = [
        {
            "date_start": "2023-09-16T13:59:07.606000+00:00",
            "driver_number": 63,
            "duration_sector_1": 26.966,
            "duration_sector_2": 38.657,
            "duration_sector_3": 26.12,
            "i1_speed": 307,
            "i2_speed": 277,
            "is_pit_out_lap": False,
            "lap_duration": 91.743,
            "lap_number": 8,
            "meeting_key": 1219,
            "segments_sector_1": [2049, 2049, 2049],
            "segments_sector_2": [2049, 2049, 2049],
            "segments_sector_3": [2048, 2048, 2048],
            "session_key": 9161,
            "st_speed": 298,
        }
    ]

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_laps(self) -> None:
        """Fetch laps returns validated Lap models."""
        respx.get(
            "https://api.openf1.org/v1/laps",
            params={"driver_number": "63", "session_key": "9161"},
        ).mock(return_value=httpx.Response(200, json=self.MOCK_LAPS))

        async with AsyncOpenF1Client() as client:
            result = await client.timing.get_laps(driver_number=63, session_key=9161)

        assert len(result) == 1
        assert result[0].lap_duration == 91.743
        assert result[0].lap_number == 8


class TestRaceEndpoint:
    """Test suite for race endpoints."""

    MOCK_STINTS: ClassVar[list[dict[str, Any]]] = [
        {
            "compound": "SOFT",
            "driver_number": 16,
            "lap_end": 20,
            "lap_start": 1,
            "meeting_key": 1219,
            "session_key": 9165,
            "stint_number": 1,
            "tyre_age_at_start": 3,
        }
    ]

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_stints(self) -> None:
        """Fetch stints returns validated Stint models."""
        respx.get(
            "https://api.openf1.org/v1/stints",
            params={"session_key": "9165"},
        ).mock(return_value=httpx.Response(200, json=self.MOCK_STINTS))

        async with AsyncOpenF1Client() as client:
            result = await client.race.get_stints(session_key=9165)

        assert len(result) == 1
        assert result[0].compound == "SOFT"


class TestCacheIntegration:
    """Test suite for cache behavior."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_cache_hit(self) -> None:
        """Second identical call should return cached result."""
        route = respx.get(
            "https://api.openf1.org/v1/car_data",
            params={"driver_number": "1"},
        ).mock(return_value=httpx.Response(200, json=MOCK_CAR_DATA))

        async with AsyncOpenF1Client(cache_ttl=60.0) as client:
            result1 = await client.telemetry.get_car_data(driver_number=1)
            result2 = await client.telemetry.get_car_data(driver_number=1)

        assert route.call_count == 1  # Only one HTTP call made
        assert len(result1) == len(result2) == 2
