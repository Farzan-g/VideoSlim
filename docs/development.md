# Development

These instructions are for people changing VideoSlim itself, not needed for
ordinary use.

## Set up a development environment

From the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

The `dev` extra includes pytest, Ruff, and mypy. FFmpeg is not installed by
this Python extra; install it separately to test real encodes.

## Tests and checks

Run tests from the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Run the linter and type checker:

```powershell
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\python.exe -m mypy src
```

On an activated macOS/Linux environment, use `pytest -q`, `ruff check .`, and
`python -m mypy src`.

The type-check command currently reports errors for optional PySide6 imports
and profile-dictionary typing. It is included as a diagnostic, not as a
passing check; CI does not run mypy. The test suite and Ruff lint are the
checks currently run by CI.

The CI workflow installs `.[dev]` and runs `pytest -q` on Ubuntu with Python
3.11. It does not install FFmpeg or test actual hardware encoding.

## Package entry points

`videoslim` is the console command registered by `pyproject.toml`. The package
can also be run as a module:

```text
python -m videoslim --help
```

The optional `gui` dependency extra installs PySide6, but does not create a
finished GUI. See [GUI status](gui.md).

## Releases

The repository's release workflow runs on version tags beginning with `v` and
builds Python distribution files with `python -m build`. It does not publish
them to a package index or create an operating-system installer.

## Project conventions

Keep core behavior independent from CLI presentation. Add focused tests for
behavior changes. For the project's existing pre-commit hooks, if pre-commit
is installed, run:

```text
pre-commit run --all-files
```

The configured hooks include Ruff lint/format checks and basic whitespace and
end-of-file cleanup.
