from __future__ import annotations

import importlib

from typer.testing import CliRunner

from videoslim.cli.app import app

runner = CliRunner()


def test_scan_command_lists_discovered_files(sample_video_dir):
    result = runner.invoke(app, ["scan", str(sample_video_dir)])

    assert result.exit_code == 0
    assert "Discovered" in result.stdout


def test_compress_executes_encoder_when_dry_run_is_disabled(sample_video_dir, monkeypatch):
    calls = []
    cli_module = importlib.import_module("videoslim.cli.app")
    monkeypatch.setattr("videoslim.core.probe.ffprobe_available", lambda: False)
    monkeypatch.setattr(cli_module, "ffmpeg_available", lambda: True)
    monkeypatch.setattr(cli_module, "encode_file", lambda request: calls.append(request))

    result = runner.invoke(
        app,
        [
            "compress",
            str(sample_video_dir),
            "--profile",
            "nvidia_hevc",
            "--no-dry-run",
        ],
    )

    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0].codec == "hevc_nvenc"
    assert calls[0].cq == 28
    assert calls[0].destination.name == "clip.compressed.mp4"
    assert "Compressed" in result.stdout
