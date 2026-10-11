from __future__ import annotations

import pytest


@pytest.fixture
def sample_video_dir(tmp_path):
    source = tmp_path / "source"
    nested = source / "nested"
    nested.mkdir(parents=True)
    clip = nested / "clip.mp4"
    clip.write_bytes(b"fake mp4")
    return source
