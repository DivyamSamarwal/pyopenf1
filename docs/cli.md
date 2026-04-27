# CLI Reference

pyopenf1 includes a command-line interface for quick data access.

## Installation

The CLI is installed automatically with the package:

```bash
pip install pyopenf1
```

## Commands

### car-data

```bash
pyopenf1 car-data --driver 1 --session 9159 --format table
pyopenf1 car-data --driver 55 --format json --output telemetry.json
```

### drivers

```bash
pyopenf1 drivers --session 9158
pyopenf1 drivers --session 9158 --format csv --output drivers.csv
```

### sessions

```bash
pyopenf1 sessions --country Belgium --year 2023
```

### laps

```bash
pyopenf1 laps --driver 63 --session 9161 --lap 8
```

### weather

```bash
pyopenf1 weather --meeting 1208
```

### stints

```bash
pyopenf1 stints --session 9165 --driver 16
```

### team-radio

```bash
pyopenf1 team-radio --session 9158 --driver 11
```

## Output Formats

| Format | Flag | Description |
|--------|------|-------------|
| Table | `--format table` | Human-readable table (default) |
| JSON | `--format json` | Pretty-printed JSON |
| CSV | `--format csv` | Comma-separated values |

## Saving Output

Use `--output <file>` to write results to a file:

```bash
pyopenf1 car-data --driver 1 --format csv --output data.csv
```
