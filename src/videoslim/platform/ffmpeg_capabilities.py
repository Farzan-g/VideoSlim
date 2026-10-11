from __future__ import annotations

import re
import shutil
import subprocess


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def ffprobe_available() -> bool:
    return shutil.which("ffprobe") is not None


def ffmpeg_version() -> str | None:
    if not ffmpeg_available():
        return None
    try:
        completed = subprocess.run(
            ["ffmpeg", "-hide_banner", "-version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    output = completed.stdout.strip().splitlines()
    return output[0] if output else "ffmpeg"


def ffprobe_version() -> str | None:
    if not ffprobe_available():
        return None
    try:
        completed = subprocess.run(
            ["ffprobe", "-hide_banner", "-version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    output = completed.stdout.strip().splitlines()
    return output[0] if output else "ffprobe"


def supported_encoders() -> list[str]:
    encoders = [
        "libx264",
        "libx265",
        "libsvtav1",
        "libaom-av1",
        "h264_nvenc",
        "hevc_nvenc",
        "h264_qsv",
        "hevc_qsv",
        "h264_amf",
        "hevc_amf",
        "copy",
    ]
    if not ffmpeg_available():
        return encoders

    try:
        completed = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"],
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return encoders

    available = set()
    output = completed.stdout or completed.stderr or ""
    for line in output.splitlines():
        match = re.search(r"\s+[VAS][A-Z.]{5}\s+([^\s]+)\s+", line)
        if match:
            available.add(match.group(1))

    discovered = [name for name in encoders if name in available or name == "copy"]
    if not discovered:
        return encoders
    return discovered
