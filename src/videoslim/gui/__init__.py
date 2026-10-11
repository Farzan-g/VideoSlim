"""Optional GUI layer. This project intentionally keeps the GUI separate from the core logic."""

from __future__ import annotations

__all__ = ["gui_available", "launch_gui"]


def gui_available() -> bool:
    try:
        import PySide6  # noqa: F401
    except ImportError:
        return False
    return True


def launch_gui() -> str:
    if not gui_available():
        raise RuntimeError("PySide6 is not installed. Install the optional GUI dependencies to launch the GUI.")
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    app.setApplicationName("VideoSlim")
    return "GUI ready"
