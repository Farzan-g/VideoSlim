# VideoSlim

VideoSlim is a local-first batch video compression tool built around Python, FFmpeg, and FFprobe. It is designed for recursive scanning, safe previewing, and configurable compression workflows without requiring cloud services or telemetry.

## What it does

- Recursively discovers candidate video files in a directory tree.
- Validates candidates with FFprobe instead of trusting file extensions alone.
- Support built-in compression profiles such as Balanced, Maximum Savings, High Quality, and Archive.
- Provides a CLI-first workflow for scanning, analyzing, compressing, and reporting.
- Keeps original files intact by default and rejects unsafe output behaviors.
- Exposes a GUI layer as an optional dependency rather than a required installation.

## Supported operating systems

- Windows: supported in the project architecture and verified through the CLI flow in this environment.
- Linux: supported by the same CLI/core architecture.
- macOS: supported in the design and optional platform hooks, but not fully runtime-verified in this environment.

## Installation

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -U pip
.venv\Scripts\python.exe -m pip install -e '.[dev]'
```

On Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
```

### FFmpeg and FFprobe requirements

Install FFmpeg and FFprobe and ensure they are on PATH. The core engine relies on them for validation and compression jobs.

- Windows: install FFmpeg from a trusted build and add the bin directory to PATH.
- Linux: install via your distribution package manager if available.
- macOS: install via Homebrew if available on the target machine.

If FFmpeg is not available, the CLI still starts and reports the missing dependency through the doctor command.

## Quick start

```bash
videoslim --help
videoslim scan /path/to/videos
videoslim analyze /path/to/videos
videoslim compress /path/to/videos --profile balanced --dry-run
videoslim doctor
```

## Built-in profiles

The project currently includes these profiles:

- balanced
- maximum_savings
- high_quality
- fast_cpu
- nvidia_hevc
- archive
- compatibility_h264

Each is validated through the profile schema before use.

## Safety defaults

- Original files are preserved unless a clearly authorized replacement policy is used.
- Output directories may not overlap the input tree in a way that would recurse into source files.
- File extension checks are treated as hints, not proof that a file is valid video.
- FFprobe validation is required before a file is accepted as a valid media candidate.
- Dry-run mode previews actions without modifying source files.

## Known limitations

- Real FFmpeg/FFprobe validation requires the binaries to be installed and available on PATH.
- Hardware encoder support depends on the installed FFmpeg build and actual host capabilities, not just GPU presence.
- The optional GUI depends on PySide6 and is not required for the CLI/core workflow.
- This project is production-minded but intentionally conservative about unsupported codecs and file types.

## Development

```bash
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m ruff check .
```

## License

VideoSlim is distributed under the MIT license. See the LICENSE file for the full text.
