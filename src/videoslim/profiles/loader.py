from __future__ import annotations

import json
from pathlib import Path

from .defaults import DEFAULT_PROFILES
from .schema import ProfileConfig


def load_profile(name: str, profile_dir: str | Path | None = None) -> dict[str, object]:
    lookup_name = name.strip()
    if profile_dir is not None:
        profile_path = Path(profile_dir) / f"{lookup_name}.json"
        if profile_path.exists():
            payload = json.loads(profile_path.read_text(encoding="utf-8"))
            validated = ProfileConfig(**payload)
            return validated.model_dump(mode="python")

    if lookup_name not in DEFAULT_PROFILES:
        raise KeyError(f"Unknown profile: {lookup_name}")

    profile = DEFAULT_PROFILES[lookup_name].copy()
    validated = ProfileConfig(**profile)
    return validated.model_dump(mode="python")


def list_builtin_profiles() -> list[str]:
    return sorted(DEFAULT_PROFILES)


def validate_profile(payload: dict[str, object]) -> ProfileConfig:
    return ProfileConfig(**payload)
