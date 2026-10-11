from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AppSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input_dir: str = "."
    output_dir: str | None = None
    preset: str = "balanced"
    scan_only: bool = True
    max_parallel_jobs: int = Field(default=2, ge=1)
    ffmpeg_path: str | None = None
    ffprobe_path: str | None = None
    logging_level: str = "INFO"
    profile_dir: str | None = None
    dry_run: bool = True
