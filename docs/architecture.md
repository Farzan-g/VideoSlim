# Project architecture

VideoSlim is a Python package with a Typer command-line application. Its
implemented workflow is: find candidate paths, optionally inspect them with
FFprobe, build output paths from a built-in profile, and invoke FFmpeg for
each file when dry-run is disabled.

## Main code areas

| Area | Location | Responsibility |
| --- | --- | --- |
| CLI | `src/videoslim/cli/` | Defines commands, parses options, and prints summaries. |
| Core | `src/videoslim/core/` | Scanning, probing, output planning, FFmpeg command construction, and encoding. |
| Profiles | `src/videoslim/profiles/` | Profile schema, built-in profile values, and profile loading/validation. |
| Configuration | `src/videoslim/config/` | Settings schema, JSON loading/writing, and default settings path. |
| Platform | `src/videoslim/platform/` | Operating-system naming and FFmpeg encoder capability checks. |
| Utilities | `src/videoslim/utils/` | Basic path, byte-formatting, and logging helpers. |
| GUI | `src/videoslim/gui/` | Optional PySide6 availability/readiness stub; no actual interface yet. |

## Compression flow

1. The CLI creates a scan configuration and recursively finds files with a
   supported extension.
2. If FFprobe is available, the scanner includes files with a video stream.
   If it is not available, extension-matched files are treated as candidates
   without media validation.
3. The selected built-in profile determines the codec, encoder preset,
   quality value, output container, and audio codec passed to the FFmpeg
   command.
4. A dry run prints planned input/output paths and stops. A real run invokes
   FFmpeg once per item, sequentially.

The CLI does not currently use the separate settings file or all profile
fields. See [configuration](configuration.md),
[profiles](profiles.md), and [codecs](codecs.md).

## Present but not connected to the user workflow

Some modules provide scaffolding rather than complete CLI features:

- Cancellation and progress state objects are not connected to compression;
  there is no interactive cancel/progress UI.
- Job summarization and statistics helpers do not provide a complete
  persistent job manager.
- Hardware profile metadata and detection stubs do not perform automatic GPU
  selection or CPU fallback.
- The GUI package does not create a usable window.
- Configuration values and imported profiles are not wired into the CLI job
  path.

These are not finished application features. Current user-visible behavior is
documented in the [CLI guide](cli.md).

## Additional core helpers

The source also contains these small internal utilities:

- `ScanConfig` carries scan settings for hidden files, symlinks, exclusions,
  and minimum/maximum file size. The CLI does not expose these settings;
  scanning currently uses their defaults. Its `extensions` field and
  `ignore_symlinks` flag are not currently consulted by the scanner.
- `VideoScanner` can be constructed in Python with a custom extension set;
  the CLI always uses the built-in extension list.
- `probe_media` calls FFprobe and returns stream/container information and
  warnings. It does not transcode or repair a file.
- `verify_output_file` checks that a result exists, meets a size threshold,
  and has a valid video stream. The CLI does not call it after encoding.
- `CancellationToken` and `ProgressState` are state holders; they are not
  connected to the active encoding loop.
- Output-directory, input-validation, summary-formatting, byte-formatting,
  and logger helpers exist for internal use. They do not add commands or
  configurable application workflows.
- `detect_hardware()` is a placeholder that currently returns `false` for
  each vendor. The CLI relies on FFmpeg's encoder listing instead.
