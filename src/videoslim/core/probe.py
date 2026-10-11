from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from .models import ProbeResult


def ffprobe_available() -> bool:
    return shutil.which("ffprobe") is not None


def probe_media(path: Path) -> ProbeResult:
    if not path.exists():
        return ProbeResult(path=path, warnings=["File does not exist."], is_valid_video=False)

    if not ffprobe_available():
        return ProbeResult(
            path=path,
            warnings=["ffprobe is not installed or not on PATH."],
            ffprobe_available=False,
            is_valid_video=False,
        )

    command = [
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_streams",
        "-show_format",
        str(path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return ProbeResult(
            path=path,
            warnings=[completed.stderr.strip() or "ffprobe reported an error."],
            ffprobe_available=True,
            is_valid_video=False,
        )

    try:
        parsed = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return ProbeResult(
            path=path,
            warnings=["ffprobe output was not valid JSON."],
            ffprobe_available=True,
            is_valid_video=False,
        )

    streams = parsed.get("streams", [])
    video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
    subtitle_streams = [stream for stream in streams if stream.get("codec_type") == "subtitle"]
    format_info = parsed.get("format", {})

    result = ProbeResult(
        path=path,
        container=format_info.get("format_name") or None,
        duration=(float(format_info.get("duration", 0.0)) if format_info.get("duration") is not None else None),
        video_streams=video_streams,
        audio_streams=audio_streams,
        subtitle_streams=subtitle_streams,
        is_valid_video=bool(video_streams),
        ffprobe_available=True,
        raw=parsed,
    )
    if not result.is_valid_video:
        result.warnings.append("File has no video stream.")
    return result
