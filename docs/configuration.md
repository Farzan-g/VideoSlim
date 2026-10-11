# Configuration

VideoSlim can create and display a JSON settings file. At present, the CLI
does not use these settings when it scans, analyzes, or compresses videos.
They are a configuration scaffold, not active controls for those commands.

## Create and view the settings file

```text
videoslim config init
videoslim config show
```

The default file is:

- Windows: `%USERPROFILE%\.videoslim\config.json`
- macOS/Linux: `~/.videoslim/config.json`

`config init` creates parent folders and writes the defaults. If the file
already exists, it overwrites it. `config show` reads this file; if no file
exists, it shows the defaults without creating a file.

## Available settings

The current settings schema accepts these fields:

| JSON field | Type | Default | Current status |
| --- | --- | --- | --- |
| `input_dir` | Text path | `"."` | Stored and shown, but CLI scan/compress commands require their own path argument. |
| `output_dir` | Text path or `null` | `null` | Stored and shown, but compression uses its `--output` option instead. |
| `preset` | Text | `"balanced"` | Stored and shown, but compression uses `--profile`. |
| `scan_only` | True/false | `true` | Stored and shown; it does not control CLI execution. |
| `max_parallel_jobs` | Integer, at least 1 | `2` | Stored and shown; compression currently processes one file at a time. |
| `ffmpeg_path` | Text path or `null` | `null` | Stored and shown; runtime lookup currently uses the `ffmpeg` command on PATH. |
| `ffprobe_path` | Text path or `null` | `null` | Stored and shown; runtime lookup currently uses the `ffprobe` command on PATH. |
| `logging_level` | Text | `"INFO"` | Stored and shown; it does not configure CLI logging. |
| `profile_dir` | Text path or `null` | `null` | Stored and shown; the CLI does not pass it to the profile loader. |
| `dry_run` | True/false | `true` | Stored and shown; compression uses `--dry-run` or `--no-dry-run`. |

The model rejects unknown JSON keys. It validates `max_parallel_jobs` as an
integer of 1 or more, but does not check that path strings point to valid
locations or that `logging_level` names a real logging level.

## Example settings file

This is the complete default shape:

```json
{
  "input_dir": ".",
  "output_dir": null,
  "preset": "balanced",
  "scan_only": true,
  "max_parallel_jobs": 2,
  "ffmpeg_path": null,
  "ffprobe_path": null,
  "logging_level": "INFO",
  "profile_dir": null,
  "dry_run": true
}
```

Editing values is allowed, but because the CLI does not currently apply this
file to jobs, change command-line options directly when running the
application. For example, pass the input folder to `compress`, select a
profile with `--profile`, choose an output with `--output`, and opt into
writing with `--no-dry-run`. See the [command-line guide](cli.md).

If the JSON cannot be read or contains an unknown field, `config show` reports
an error instead of silently ignoring it.
