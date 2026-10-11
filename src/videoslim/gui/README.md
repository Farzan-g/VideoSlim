# GUI package status

This package does not yet contain a graphical interface. It is currently a
small optional-dependency stub:

- `gui_available()` reports whether PySide6 can be imported.
- `launch_gui()` creates or retrieves a `QApplication` and returns `GUI ready`.
- No window, event loop, file picker, scan workflow, progress display, or
  compression controls are implemented.

Install the optional dependency from the project root with:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[gui]"
```

There is no supported end-user GUI launch command. Use the command-line
application documented in [`docs/cli.md`](../../../docs/cli.md). See
[`docs/gui.md`](../../../docs/gui.md) for the user-facing status.
