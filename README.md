# VideoSlim

VideoSlim is a command-line program for finding videos in a folder and making
compressed copies with FFmpeg. It can scan folders and subfolders, preview
which files it will process, inspect video files, and write compressed results
without replacing the originals.

> **Important:** compression previews are the default. Add `--no-dry-run` only
> when you are ready to create output files. Use a separate output folder to
> keep the original videos easy to find.

## Get started

1. Install Python 3.11 or newer and FFmpeg. FFmpeg includes the `ffprobe`
   companion program used to inspect videos. Follow the
   [step-by-step installation guide](docs/installation.md).
2. Open a terminal in the VideoSlim project folder and install the app in its
   own Python environment. On Windows, use PowerShell:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -e .
   ```

3. Check that the app and video tools are available:

   ```powershell
   .\.venv\Scripts\videoslim doctor
   ```

4. Preview the videos in a folder. Put quotation marks around paths that
   contain spaces:

   ```powershell
   $source = "$HOME\Videos"
   .\.venv\Scripts\videoslim compress $source --profile balanced --dry-run
   ```

5. When the preview looks right, create compressed copies in another folder:

   ```powershell
   $source = "$HOME\Videos"
   $output = "$HOME\Videos_Compressed"
   .\.venv\Scripts\videoslim compress $source --output $output --profile balanced --no-dry-run
   ```

   The program creates the output folder as needed. It keeps each video's
   subfolder structure and leaves the source files in place.

If you activate `.venv` first, you can use `videoslim` instead of the longer
`.venv\Scripts\videoslim` path. See the [CLI guide](docs/cli.md) for all
commands and examples.

## What VideoSlim can do

- Recursively scan folders for common video file types.
- Inspect recognized files with FFprobe when it is installed.
- Preview compression tasks without writing compressed files.
- Compress files one at a time with a built-in profile and FFmpeg.
- Write results beside the source files or under a separate output folder.
- Show FFmpeg, FFprobe, and encoder availability with `doctor`.
- Validate, import, export, list, and show profile data through CLI commands.
- Create a JSON diagnostic report.

This is an early-stage, CLI-first project. See
[what is not finished](docs/troubleshooting.md#current-limitations) before
relying on it for unattended or archival work.

## Guides

- [Installation and setup](docs/installation.md)
- [Command-line reference](docs/cli.md)
- [Compression profiles](docs/profiles.md)
- [Codecs and hardware acceleration](docs/codecs.md)
- [Configuration file](docs/configuration.md)
- [Troubleshooting and limitations](docs/troubleshooting.md)
- [GUI status](docs/gui.md)
- [Project scripts](docs/scripts.md)
- [Architecture](docs/architecture.md)
- [Development and tests](docs/development.md)

## Supported operating systems

The code includes Windows, Linux, and macOS platform detection. The command
line is the implemented user interface. The CI test workflow currently runs on
Ubuntu with Python 3.11; other operating systems and Python versions should be
treated as not fully verified.

## License

VideoSlim is distributed under the MIT license. See [LICENSE](LICENSE).
