# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-27

### Added
- Initial release of `pyopenf1`.
- `AsyncOpenF1Client` — fully async client with `async with` context manager support.
- `OpenF1Client` — synchronous wrapper for non-async usage.
- Full coverage of all 18 OpenF1 API endpoints:
  - Car data, Location (telemetry)
  - Sessions, Meetings
  - Drivers
  - Laps, Intervals, Positions (timing)
  - Race control, Pit stops, Stints, Overtakes (race)
  - Drivers championship, Teams championship
  - Session results, Starting grid
  - Weather
  - Team radio
- Pydantic V2 models with frozen immutability for all endpoints.
- Automatic retry with exponential backoff on 429/5xx errors via `tenacity`.
- Client-side rate limiter (token-bucket) to preempt 429 responses.
- Optional in-memory TTL cache for responses.
- Structured logging via `logging.getLogger("pyopenf1")`.
- Custom exception hierarchy: `PyOpenF1Error` → `APIError` → `RateLimitError`, `AuthenticationError`, `NotFoundError`, `ServerError`.
- CLI tool: `pyopenf1 <endpoint> --driver N --session N`.
- Optional pandas DataFrame integration via `pyopenf1.ext.pandas.to_dataframe()`.
- PEP 561 typed package (`py.typed` marker).
- GitHub Actions CI (Ruff, mypy, pytest) and PyPI publish workflows.
- Pre-commit hooks configuration.
- mkdocs-material documentation site.

[Unreleased]: https://github.com/DivyamSamarwal/pyopenf1/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/DivyamSamarwal/pyopenf1/releases/tag/v0.1.0
