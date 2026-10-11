import json
from pathlib import Path

import pytest

from videoslim.config.loader import load_config
from videoslim.profiles.defaults import DEFAULT_PROFILES
from videoslim.profiles.loader import load_profile


def test_default_profiles_include_required_profiles() -> None:
    required = {
        "balanced",
        "maximum_savings",
        "high_quality",
        "fast_cpu",
        "nvidia_hevc",
        "archive",
        "compatibility_h264",
    }
    assert required.issubset(DEFAULT_PROFILES)


def test_load_profile_returns_valid_profile_data() -> None:
    profile = load_profile("balanced")
    assert profile["name"] == "balanced"
    assert profile["codec"]


def test_load_profile_rejects_unknown_profile() -> None:
    with pytest.raises(KeyError):
        load_profile("missing-profile")


def test_load_config_reads_json_file(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"preset": "high_quality", "max_parallel_jobs": 3}), encoding="utf-8")

    config = load_config(config_path)
    assert config.preset == "high_quality"
    assert config.max_parallel_jobs == 3
