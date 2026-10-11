from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from .models import VideoFile


def build_plan(
    files: Iterable[VideoFile],
    preset: str = "balanced",
    output_dir: str | Path | None = None,
) -> list[dict[str, object]]:
    plan: list[dict[str, object]] = []
    for item in files:
        source_path = item.path
        if output_dir is None:
            destination = source_path.with_suffix(".compressed.mp4")
        else:
            destination = Path(output_dir) / item.relative_path
            destination = destination.with_suffix(".compressed.mp4")
        plan.append({
            "source": source_path,
            "output": destination,
            "preset": preset,
            "size_bytes": item.file_size,
        })
    return plan
