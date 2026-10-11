# Install and set up VideoSlim

These instructions install VideoSlim from its source folder. VideoSlim does
not currently provide a graphical installer.

## 1. Get the project

Get the source ZIP from the repository page you were given and extract it.
If Git is installed and you have access to the repository, use its clone URL:

```text
git clone <repository-url>
cd <repository-folder>
```

Replace the placeholders with the clone URL and folder name provided by the
project owner; they are not commands to type literally. If the repository
page is private, sign in or ask the owner for access. If you downloaded a ZIP,
open PowerShell or another terminal in the extracted project folder instead.
The folder should contain `pyproject.toml`.

## 2. Install Python

Install Python 3.11 or newer. On Windows, the Python installer can be
downloaded from [python.org](https://www.python.org/downloads/). Enable the
installer option that adds Python to PATH if it is offered.

Check the installation in PowerShell:

```powershell
py --version
```

On macOS or Linux, use:

```bash
python3 --version
```

## 3. Install FFmpeg and FFprobe

FFmpeg does the video encoding. FFprobe, distributed with FFmpeg, reads video
information so VideoSlim can filter out files that are not valid videos.
VideoSlim can start without these programs, but compression requires FFmpeg.

### Windows

If `winget` is available, open PowerShell and run:

```powershell
winget install --id Gyan.FFmpeg --source winget
```

Close and reopen PowerShell after installation so it reloads PATH. Check both
programs:

```powershell
ffmpeg -version
ffprobe -version
```

If PowerShell says a command is not recognized, add the FFmpeg `bin` folder to
your Windows user PATH, then open a new terminal. The exact folder depends on
where FFmpeg was installed.

### macOS

With Homebrew installed:

```bash
brew install ffmpeg
ffmpeg -version
ffprobe -version
```

### Ubuntu or Debian Linux

```bash
sudo apt update
sudo apt install ffmpeg
ffmpeg -version
ffprobe -version
```

Other Linux distributions may use a different package manager. Install an
FFmpeg package that includes FFprobe and make sure both commands are on PATH.

### NVIDIA hardware encoding

The `nvidia_hevc` profile needs an FFmpeg build that includes the `hevc_nvenc`
encoder, a supported NVIDIA GPU, and a working NVIDIA driver. To check whether
the installed FFmpeg lists the encoder:

```powershell
ffmpeg -hide_banner -encoders | Select-String hevc_nvenc
```

On macOS or Linux, use `grep hevc_nvenc` instead of `Select-String`. A listed
encoder does not guarantee that the GPU driver can start an encode; a real
compression test is needed to confirm that.

## 4. Create a Python environment and install VideoSlim

A Python environment keeps VideoSlim's installed packages separate from other
Python applications.

### Windows PowerShell

From the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
```

You can activate the environment for the current PowerShell window:

```powershell
.\.venv\Scripts\Activate.ps1
videoslim --help
```

If script execution policy prevents activation, do not change the policy just
for VideoSlim. Run commands using the full executable path instead:
`.\.venv\Scripts\videoslim`.

### macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
videoslim --help
```

The `-e` option installs the project in editable mode, so changes to the
project source are used without reinstalling it.

## 5. Check the installation

With the environment active, run:

```text
videoslim doctor
```

Or, on Windows without activating the environment:

```powershell
.\.venv\Scripts\videoslim doctor
```

The command prints JSON showing the Python version, operating system, whether
FFmpeg and FFprobe can be found, the encoders detected in FFmpeg, and the
built-in profile names. It does not encode a video.

For command examples, continue to the [CLI guide](cli.md). For common errors,
see [troubleshooting](troubleshooting.md).

## Optional development packages

If you want to run the tests and linter while working on VideoSlim, install
the development extra instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

The optional `gui` extra installs PySide6:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[gui]"
```

PySide6 installation alone does **not** provide a usable graphical interface;
see [GUI status](gui.md).
