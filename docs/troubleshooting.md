# Troubleshooting

Start by checking the installation:

```text
videoslim doctor
```

On Windows, if the environment is not active, run
`.\.venv\Scripts\videoslim doctor` from the project folder. The output is JSON
and reports whether VideoSlim can find FFmpeg and FFprobe.

## “videoslim is not recognized”

The Python environment may not be active, or VideoSlim may not have been
installed into it. From the project folder, run:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\videoslim --help
```

Alternatively activate the environment first:

```powershell
.\.venv\Scripts\Activate.ps1
videoslim --help
```

## “ffmpeg is not installed or not available on PATH”

Install FFmpeg, then close and reopen the terminal. Check:

```text
ffmpeg -version
ffprobe -version
```

If the commands still are not recognized, add the folder containing
`ffmpeg.exe` and `ffprobe.exe` to PATH, then reopen the terminal or VS Code.
See [installation](installation.md#3-install-ffmpeg-and-ffprobe).

Dry-run previews do not require FFmpeg. Actual compression does.

## A scan finds no files

VideoSlim only looks for these extensions: `.mp4`, `.mkv`, `.mov`, `.avi`,
`.webm`, `.m4v`, `.mpg`, `.mpeg`, `.ts`, `.mts`, `.m2ts`, `.wmv`, `.flv`, and
`.3gp`. It searches recursively but skips hidden files/folders (names starting
with a dot) and does not follow symbolic links.

If FFprobe is installed, files without a video stream are excluded. If it is
missing, supported extensions are shown as candidates without validation.
Run `videoslim doctor` to check the tool installation, and quote paths
containing spaces. For example:

```powershell
videoslim scan "C:\Users\YourName\Videos"
```

## “The output directory overlaps with the input directory”

The output cannot be the same folder as the input or a folder inside it,
because a recursive scan could then encounter its own outputs. Choose a
separate destination, such as:

```powershell
videoslim compress "C:\Videos" --output "C:\Videos_Compressed" --profile balanced --dry-run
```

## Unknown profile

Use `videoslim profiles list` to see the built-in names. Names use
underscores, for example `nvidia_hevc` and `maximum_savings`.

Custom profile import is incomplete: the command stores the profile but the
CLI does not load imported profiles for compression. See
[profiles](profiles.md#import-and-custom-profiles-incomplete).

## A profile file fails validation

The profile schema rejects unknown top-level keys. The repository file
`profiles/compatibility_h264.json`, for example, contains `pixel_format`, a
field the current schema does not accept. Use
`videoslim profiles show compatibility_h264` to see the canonical built-in
data, or export a built-in profile before editing it.

## NVIDIA encoding fails

Check that `videoslim doctor` lists `hevc_nvenc`. If it does not, FFmpeg may
not include NVENC, or the current terminal may still have an old PATH. If it
does list the encoder but compression fails, update/install the NVIDIA driver
and try a short sample. Encoder-list availability does not guarantee that the
GPU and driver can initialize an encode.

The current application stops when NVENC fails; the profile's declared
CPU-fallback setting is not implemented. To use the CPU instead, choose a CPU
profile such as `balanced` or `fast_cpu`.

## Compression stops or an output is unexpected

VideoSlim processes files sequentially. The first FFmpeg error stops the
command; the remaining files are not attempted. Read the FFmpeg error shown in
the terminal and test that source file separately.

VideoSlim asks FFmpeg to overwrite existing destinations. Use a new output
folder if you need to keep earlier results. Source videos are not deleted.
Compression is not guaranteed to reduce file size, and current encoding does
not implement all declared audio-track, subtitle, metadata, or resolution
preservation settings. Compare outputs with their sources before relying on
them.

## Profile/config settings seem to have no effect

`config init` and `config show` read and write a settings file, but the CLI
does not apply its values to scan/compress commands. Use command-line
arguments instead. Similarly, some fields accepted in a profile JSON are not
used by the encoder. See [configuration](configuration.md) and
[codecs](codecs.md).

## Current limitations

The following features are incomplete or not implemented as user-facing
features:

- The optional PySide6 GUI package contains only a readiness stub; there is no
  window or interactive graphical workflow.
- Imported custom profiles are saved but are not selectable by the CLI.
- The settings file is not connected to CLI jobs.
- Profile fields for fallback, multiple audio tracks, subtitles, metadata,
  resolution scaling, target bitrate, and hardware permissions are not
  applied by the encoder.
- CPU fallback after hardware-encoder failure is not implemented.
- Compression runs sequentially, stops on the first error, and has no
  batch-resume or per-file retry feature.
- There are no standalone helper scripts in the repository.
- The CI workflow tests on Ubuntu with Python 3.11; Windows, macOS, and other
  Python versions are not fully verified by CI.

Do not treat VideoSlim as a finished archival, unattended batch, or
lossless-preservation system.
