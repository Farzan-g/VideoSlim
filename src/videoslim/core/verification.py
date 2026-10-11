from __future__ import annotations

from pathlib import Path

from .probe import probe_media


def verify_output_file(path: str | Path, *, min_size_bytes: int = 1) -> bool:
    target = Path(path)
    if not target.exists() or not target.is_file():
        return False

    size = target.stat().st_size
    if size < min_size_bytes:
        return False

    result = probe_media(target)
    if not getattr(result, "ffprobe_available", True):
        return False
    return getattr(result, "is_valid_video", False)
