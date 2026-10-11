import pytest

from videoslim.core.scanner import ScanConfig, VideoScanner
from videoslim.core.verification import verify_output_file


def test_scan_config_rejects_invalid_overlap(tmp_path):
    input_dir = tmp_path / "inputs"
    output_dir = tmp_path / "inputs" / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    with pytest.raises(ValueError):
        ScanConfig(input_dir=input_dir, output_dir=output_dir)


def test_scan_config_allows_valid_output_path(tmp_path):
    input_dir = tmp_path / "inputs"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    config = ScanConfig(input_dir=input_dir, output_dir=output_dir)
    assert config.input_dir == input_dir
    assert config.output_dir == output_dir


def test_scanner_detects_video_extensions():
    scanner = VideoScanner()
    assert ".mp4" in scanner.video_extensions
    assert ".mkv" in scanner.video_extensions


def test_scanner_builds_relative_output_path(tmp_path):
    input_dir = tmp_path / "movie"; input_dir.mkdir()
    (input_dir / "nested").mkdir()
    video = input_dir / "nested" / "clip.mp4"
    video.write_bytes(b"fake")

    output_dir = tmp_path / "out"
    relative = VideoScanner().relative_output_path(video, input_dir, output_dir)

    assert relative == output_dir / "nested" / "clip.mp4"


def test_scanner_requires_ffprobe_validation_for_mp4_candidates(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    fake_video = input_dir / "not_really_video.mp4"
    fake_video.write_text("This is not a valid video file", encoding="utf-8")

    def fake_run(command, capture_output, text, check, timeout=None):
        return type(
            "Completed",
            (),
            {"returncode": 0, "stdout": '{"streams": [{"codec_type": "audio"}]}'},
        )()

    monkeypatch.setattr("videoslim.core.probe.ffprobe_available", lambda: True)
    monkeypatch.setattr("subprocess.run", fake_run)

    files = VideoScanner().scan_directory(ScanConfig(input_dir=input_dir))
    assert files == []


def test_verify_output_file_requires_valid_video_stream(tmp_path, monkeypatch):
    output = tmp_path / "bad-output.mp4"
    output.write_bytes(b"not a real video")

    monkeypatch.setattr(
        "videoslim.core.verification.probe_media",
        lambda path: type("Probe", (), {"is_valid_video": False, "warnings": ["No video stream"]})(),
    )

    assert not verify_output_file(output)
