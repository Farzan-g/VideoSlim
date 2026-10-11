from __future__ import annotations

from pathlib import Path

from videoslim.core.models import ScanConfig
from videoslim.core.scanner import VideoScanner


def scan_directory(path: str | Path, output: str | Path | None = None) -> list[str]:
    config = ScanConfig(input_dir=Path(path), output_dir=Path(output) if output else None)
    discovered = VideoScanner().scan_directory(config)
    return [str(item.relative_path) for item in discovered]
