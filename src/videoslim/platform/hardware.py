from __future__ import annotations

import platform


def hardware_profiles() -> dict[str, list[str]]:
    profiles: dict[str, list[str]] = {
        "nvidia": ["h264_nvenc", "hevc_nvenc", "av1_nvenc"],
        "intel": ["h264_qsv", "hevc_qsv", "av1_qsv"],
        "amd": ["h264_amf", "hevc_amf"],
        "apple": ["h264_videotoolbox", "hevc_videotoolbox"],
    }
    if platform.system() == "Darwin":
        profiles["default"] = profiles["apple"]
    return profiles


def detect_hardware() -> dict[str, bool]:
    detected = {"nvidia": False, "intel": False, "amd": False, "apple": False}
    # This intentionally does not infer capability from a GPU model alone.
    # Real availability is validated using FFmpeg encoder support in ffmpeg_capabilities.
    return detected
