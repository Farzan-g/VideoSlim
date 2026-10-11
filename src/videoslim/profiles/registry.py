from __future__ import annotations

from pathlib import Path

from .defaults import DEFAULT_PROFILES
from .loader import load_profile


def builtin_profile_names() -> list[str]:
    return sorted(DEFAULT_PROFILES)


def profile_exists(name: str) -> bool:
    return name in DEFAULT_PROFILES


def load_builtin_profile(name: str) -> dict[str, object]:
    return load_profile(name)


def export_profile_to_file(name: str, output_path: str | Path) -> Path:
    payload = load_builtin_profile(name)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(__import__("json").dumps(payload, indent=2), encoding="utf-8")
    return target
