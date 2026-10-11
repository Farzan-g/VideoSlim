from __future__ import annotations

from videoslim.platform import ffmpeg_capabilities


def test_supported_encoders_parses_ffmpeg_encoder_flags(monkeypatch):
    monkeypatch.setattr(ffmpeg_capabilities, "ffmpeg_available", lambda: True)
    monkeypatch.setattr(
        ffmpeg_capabilities.subprocess,
        "run",
        lambda *args, **kwargs: type(
            "Completed",
            (),
            {
                "returncode": 0,
                "stdout": (
                    " V....D libx264 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10\n"
                    " V....D hevc_nvenc NVIDIA NVENC hevc encoder\n"
                    " A..... aac AAC (Advanced Audio Coding)\n"
                ),
                "stderr": "",
            },
        )(),
    )

    assert ffmpeg_capabilities.supported_encoders() == [
        "libx264",
        "hevc_nvenc",
        "copy",
    ]
