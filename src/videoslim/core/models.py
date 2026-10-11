from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ScanConfig:
    input_dir: Path
    output_dir: Path | None = None
    extensions: tuple[str, ...] = (
        ".mp4",
        ".mkv",
        ".mov",
        ".avi",
        ".webm",
        ".m4v",
        ".mpg",
        ".mpeg",
        ".ts",
        ".mts",
        ".m2ts",
        ".wmv",
        ".flv",
        ".3gp",
    )
    exclude_globs: tuple[str, ...] = ()
    follow_symlinks: bool = False
    include_hidden: bool = False
    min_size_bytes: int | None = None
    max_size_bytes: int | None = None
    ignore_symlinks: bool = True
    scan_only: bool = True

    def __post_init__(self) -> None:
        self.input_dir = Path(self.input_dir).resolve()
        if self.output_dir is not None:
            self.output_dir = Path(self.output_dir).resolve()
            if self.output_overlaps_input():
                raise ValueError(
                    "The output directory overlaps with the input directory and would recurse into source files."
                )

    def output_overlaps_input(self) -> bool:
        if self.output_dir is None:
            return False
        try:
            return self.output_dir == self.input_dir or self.output_dir.is_relative_to(self.input_dir)
        except ValueError:
            return False


@dataclass(slots=True)
class VideoFile:
    path: Path
    relative_path: Path
    file_size: int
    extension: str
    discovered_by_hint: bool = True
    is_valid_video: bool = False
    probe_summary: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class ProbeResult:
    path: Path
    container: str | None = None
    duration: float | None = None
    video_streams: list[dict[str, object]] = field(default_factory=list)
    audio_streams: list[dict[str, object]] = field(default_factory=list)
    subtitle_streams: list[dict[str, object]] = field(default_factory=list)
    is_valid_video: bool = False
    ffprobe_available: bool = False
    warnings: list[str] = field(default_factory=list)
    raw: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class JobSummary:
    files_discovered: int = 0
    files_processed: int = 0
    files_skipped: int = 0
    total_input_bytes: int = 0
    total_output_bytes: int = 0
    warnings: list[str] = field(default_factory=list)
