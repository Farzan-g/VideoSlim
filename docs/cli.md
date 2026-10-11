# Command-line guide

VideoSlim is operated from a terminal. A terminal is a text window where you
type commands. On Windows, use PowerShell; on macOS or Linux, use Terminal.

Start by opening the terminal in the project folder. If the Python environment
is active, commands begin with `videoslim`. If it is not active on Windows,
prefix commands with `.\.venv\Scripts\videoslim`.

In examples, replace `C:\Users\YourName\Videos` with the folder on your
computer. Put a path in quotation marks when it contains spaces.

## Find help

```text
videoslim --help
videoslim compress --help
videoslim profiles --help
videoslim config --help
```

`--help` prints command names and available options without running the
operation.

## Scan a folder

```powershell
videoslim scan "C:\Users\YourName\Videos"
```

VideoSlim searches the folder and its subfolders for files with these
extensions: `.mp4`, `.mkv`, `.mov`, `.avi`, `.webm`, `.m4v`, `.mpg`, `.mpeg`,
`.ts`, `.mts`, `.m2ts`, `.wmv`, `.flv`, and `.3gp`. If FFprobe is available,
files without a valid video stream are excluded. Without FFprobe, files with a
recognized extension are listed as candidates; some may not actually be
videos. The command displays at most the first 20 file paths.

Options:

| Option | Default | Meaning |
| --- | --- | --- |
| `--output PATH` | None | Checks the output path for safety. It does not create files or change the scan destination. The same path-safety rule applies to compression: output cannot be the input folder or a folder inside it. |
| `--preset NAME` | `balanced` | Changes the preset name printed in the scan summary only. It does not load or apply a profile during scanning. |

## Analyze a folder

```powershell
videoslim analyze "C:\Users\YourName\Videos"
```

This scans for candidate files and probes them, then prints a valid/invalid
summary. Install FFprobe for meaningful analysis. If FFprobe is missing,
candidate files cannot be confirmed as valid videos, so they are counted as
invalid by this command. When FFprobe is available, the scanner filters out
invalid files before this command counts candidates, so the invalid count may
not include every rejected file.

## Preview or compress

First preview the plan:

```powershell
$source = "$HOME\Videos"
videoslim compress $source --profile balanced --dry-run
```

Then, when the list looks right, write compressed copies in a separate folder:

```powershell
$source = "$HOME\Videos"
$output = "$HOME\Videos_Compressed"
videoslim compress $source --output $output --profile balanced --no-dry-run
```

In PowerShell, assigning a folder to a variable makes it easier to reuse a
long path. Alternatively, replace `$source` and `$output` with quoted full
paths such as `"C:\Users\Alex\My Videos"`.

Options:

| Option | Default | Meaning |
| --- | --- | --- |
| `--output PATH` | None | Puts each result under this folder and keeps the input's subfolder layout. The folder is created when needed. It must not be the input folder or inside it. |
| `--profile NAME` | `balanced` | Selects one built-in profile. See [profiles](profiles.md). |
| `--dry-run` / `--no-dry-run` | `--dry-run` | Preview paths only, or actually run FFmpeg and write files. Compression requires FFmpeg. |

Without `--output`, compressed files are written beside each source with
`.compressed` added to the filename, for example
`clip.mp4` becomes `clip.compressed.mp4`. An output directory is safer for
large batches because it keeps results separate.

Important behavior:

- The original source is not removed.
- VideoSlim processes files one at a time. The `max_parallel_jobs` setting
  does not change this.
- If you write results beside sources, a later scan can treat the existing
  `.compressed` files as new inputs. Prefer a separate output folder and do
  not include that folder in a future input scan.
- FFmpeg is called with overwrite enabled. If a planned destination already
  exists, it can be replaced.
- If encoding one file fails, the command stops at that error; it does not
  continue through the remaining files or automatically switch encoders.
- Compression does not guarantee a smaller result. Compare the output and
  source sizes before deleting anything yourself.
- Only the first 20 planned file pairs are printed before processing.

## Manage profiles

```text
videoslim profiles list
videoslim profiles show balanced
videoslim profiles validate PATH
videoslim profiles import PATH
videoslim profiles export NAME
```

Examples:

```powershell
videoslim profiles list
videoslim profiles show nvidia_hevc
videoslim profiles validate ".\my-profile.json"
videoslim profiles export balanced --output ".\balanced.json"
```

`validate` checks that a JSON file can be parsed as the profile schema.
`import` validates the file and copies it to the user's
`~/.videoslim/profiles` folder (`%USERPROFILE%\.videoslim\profiles` on Windows).
`export` writes a built-in profile to a JSON file; its default output is
`profile-export.json` in the current folder.

**Limitation:** imported profiles are not currently loaded by the CLI's
compression or `profiles show` commands. Those commands load built-in profiles
only. The import command saves a profile but does not make it usable for
compression yet. See [profiles](profiles.md).

## Manage settings

```text
videoslim config init
videoslim config show
```

`config init` writes a starter JSON file to
`%USERPROFILE%\.videoslim\config.json` on Windows or
`~/.videoslim/config.json` on macOS/Linux. Running it again overwrites that
file. `config show` prints the settings currently loaded from that file, or
the defaults if the file does not exist.

**Limitation:** the current CLI does not load these settings when scanning,
analyzing, or compressing. Editing the file does not change those operations
yet. See [configuration](configuration.md).

## Diagnostics, report, and version

```text
videoslim doctor
videoslim report ".\videoslim-report.json"
videoslim version
```

- `doctor` prints runtime and encoder information as JSON.
- `report PATH` creates or overwrites a JSON diagnostic report at `PATH`.
  The report contains a schema version, UTC generation time, built-in profile
  names, and FFmpeg/FFprobe availability. It does not include scanned video
  details.
- `version` prints the current application version.

## Shell completion

The top-level CLI also provides Typer's `--install-completion` and
`--show-completion` options. These install or display completion instructions
for the shell. Consult `videoslim --help` for the options shown by your
installed Typer version.
