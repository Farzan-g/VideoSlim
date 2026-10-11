from __future__ import annotations

from pathlib import Path


def safe_join(base: Path, relative: str | Path) -> Path:
    return (base / relative).resolve()
