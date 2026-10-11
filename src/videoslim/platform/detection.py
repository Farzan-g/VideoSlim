from __future__ import annotations

import platform


def platform_name() -> str:
    return platform.system().lower()


def is_windows() -> bool:
    return platform_name() == "windows"


def is_linux() -> bool:
    return platform_name() == "linux"


def is_macos() -> bool:
    return platform_name() == "darwin"
