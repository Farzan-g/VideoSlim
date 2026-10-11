from __future__ import annotations

from collections.abc import Iterable


def render_file_list(files: Iterable[str]) -> str:
    return "\n".join(f"- {item}" for item in files)
