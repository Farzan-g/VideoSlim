from __future__ import annotations

from pathlib import Path


def validate_input_directory(path: str | Path) -> Path:
    chosen = Path(path)
    if not chosen.exists():
        raise FileNotFoundError(f"Input directory does not exist: {chosen}")
    if not chosen.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {chosen}")
    return chosen


def validate_output_directory(path: str | Path | None) -> Path | None:
    if path is None:
        return None
    return Path(path)
