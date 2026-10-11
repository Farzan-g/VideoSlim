from __future__ import annotations

from typer.testing import CliRunner

from videoslim.cli.app import app

runner = CliRunner()


def test_scan_command_lists_discovered_files(sample_video_dir):
    result = runner.invoke(app, ["scan", str(sample_video_dir)])

    assert result.exit_code == 0
    assert "Discovered" in result.stdout
