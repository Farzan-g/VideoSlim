from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from .models import VideoFile


def build_plan(
    files: Iterable[VideoFile],
    preset: str = "balanced",
    output_dir: str | Path | None = None,
    container: str = "mp4",
) -> list[dict[str, object]]:
    extension = container.lstrip(".")
    if not extension or any(separator in extension for separator in ("/", "\\")):
        raise ValueError("The output container must be a file extension.")

    plan: list[dict[str, object]] = []
    for item in files:
        source_path = item.path
        if output_dir is None:
            destination = source_path.with_suffix(f".compressed.{extension}")
        else:
            destination = Path(output_dir) / item.relative_path
            destination = destination.with_suffix(f".compressed.{extension}")
        plan.append({
            "source": source_path,
            "output": destination,
            "preset": preset,
            "size_bytes": item.file_size,
        })
    return plan
