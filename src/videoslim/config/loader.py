from __future__ import annotations

import json
from pathlib import Path

from .schema import AppSettings


def load_config(path: str | Path | None = None) -> AppSettings:
    if path is None:
        return AppSettings()

    config_path = Path(path)
    if not config_path.exists():
        return AppSettings()

    payload = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"Configuration file must contain a JSON object: {config_path}")
    return AppSettings(**payload)


def save_default_config(path: str | Path, *, include_template: bool = True) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    defaults = AppSettings()
    payload = defaults.model_dump(mode="python")
    if include_template:
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return target
