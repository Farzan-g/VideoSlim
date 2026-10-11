# Installation

## Local development

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

## Runtime requirements

- Python 3.11+
- FFmpeg and FFprobe installed and available on PATH for validation and compression jobs
- Optional hardware encoder support depends on the installed FFmpeg build and the host hardware

## Diagnostics

```bash
videoslim doctor
```

This command reports Python, FFmpeg/FFprobe availability, supported encoders, and profile metadata.
