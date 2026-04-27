# Command Line Interface (CLI)

`pyopenf1` includes a powerful CLI tool that allows you to fetch OpenF1 data directly from your terminal, without writing any Python code.

## Usage

```bash
pyopenf1 <endpoint> [options]
```

## Output Formats

The CLI can output data in three formats using the `--format` flag.

=== "Table (Default)"
    Rich, human-readable terminal tables.
    ```console
    $ pyopenf1 drivers --session 9158 --format table
    
    ┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
    ┃ Driver Number ┃ Name           ┃ Team             ┃
    ┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
    │ 1             │ Max Verstappen │ Red Bull Racing  │
    │ 4             │ Lando Norris   │ McLaren          │
    └───────────────┴────────────────┴──────────────────┘
    ```

=== "JSON"
    Perfect for piping into `jq` or saving to files.
    ```console
    $ pyopenf1 car-data --driver 1 --session 9159 --format json > telemetry.json
    ```

=== "CSV"
    Perfect for opening in Excel or importing into a database.
    ```console
    $ pyopenf1 laps --driver 63 --session 9161 --format csv > russell_laps.csv
    ```

## Filtering

You can pass standard OpenF1 filtering parameters as flags:

```bash
pyopenf1 weather --meeting 1208
pyopenf1 telemetry --driver 1 --session 9159
```
