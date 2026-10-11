# Project scripts and launch commands

There is no `scripts/` folder and the repository contains no standalone
PowerShell, batch, shell, or helper automation scripts.

The supported launch points are installed Python entry points:

```text
videoslim COMMAND
python -m videoslim COMMAND
```

The `videoslim` command is registered in `pyproject.toml` and starts
`videoslim.cli.app:app`. `python -m videoslim` uses the package's
`__main__.py` and starts the same CLI. On Windows, if the virtual environment
is not activated, use:

```powershell
.\.venv\Scripts\videoslim --help
```

The optional GUI module is not a launch script or a completed graphical
application; see [GUI status](gui.md). Development test and lint commands are
listed in [development](development.md).
