# GUI status

VideoSlim does not currently have an interactive graphical interface. The
actual user-facing application is the command line; start with the
[installation guide](installation.md) and [CLI guide](cli.md).

The `gui` optional dependency extra installs PySide6:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[gui]"
```

However, installing PySide6 does not add a GUI command or window. The module
`videoslim.gui` only checks whether PySide6 can be imported. Its
`launch_gui()` function creates or retrieves a `QApplication` and returns the
text `GUI ready`; it does not create a window, run the application event loop,
or provide scan/compression controls. This is a readiness placeholder, not a
usable GUI feature.

There is no supported graphical launch command. Use the CLI instead.
