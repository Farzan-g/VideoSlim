from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .command_builder import build_ffmpeg_command


@dataclass(slots=True)
class EncodeRequest:
    source: Path
    destination: Path
    preset: str = "balanced"
    codec: str = "libx264"
    dry_run: bool = True
    ffmpeg_path: str = "ffmpeg"
    crf: int = 28
    cq: int | None = None
    audio_codec: str = "aac"
    extra_args: list[str] | None = None


def encode_file(request: EncodeRequest) -> bool:
    if request.dry_run:
        return True
    if not request.source.exists():
        raise FileNotFoundError(request.source)

    ffmpeg_bin = request.ffmpeg_path or shutil.which("ffmpeg") or "ffmpeg"
    if shutil.which(ffmpeg_bin) is None and ffmpeg_bin == "ffmpeg":
        raise RuntimeError("ffmpeg is not installed or not available on PATH.")

    command = build_ffmpeg_command(
        request.source,
        request.destination,
        codec=request.codec,
        preset=request.preset,
        crf=request.crf,
        cq=request.cq,
        audio_codec=request.audio_codec,
        extra_args=request.extra_args,
    )
    command[0] = ffmpeg_bin

    request.destination.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        stderr = (completed.stderr or completed.stdout or "").strip()
        raise RuntimeError(stderr or "FFmpeg failed without diagnostic output.")
    return True
