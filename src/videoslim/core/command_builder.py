from __future__ import annotations

from pathlib import Path


def build_ffmpeg_command(
    source: Path,
    destination: Path,
    *,
    codec: str = "libx264",
    preset: str = "medium",
    crf: int = 28,
    audio_codec: str = "aac",
    extra_args: list[str] | None = None,
) -> list[str]:
    args = [
        "ffmpeg",
        "-y",
        "-i",
        str(source),
        "-c:v",
        codec,
        "-preset",
        preset,
        "-crf",
        str(crf),
        "-c:a",
        audio_codec,
    ]
    if extra_args:
        args.extend(extra_args)
    args.append(str(destination))
    return args
