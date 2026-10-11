from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from videoslim.config.loader import load_config, save_default_config
from videoslim.config.paths import default_config_path
from videoslim.core.encoder import EncodeRequest, encode_file
from videoslim.core.models import ScanConfig
from videoslim.core.planner import build_plan
from videoslim.core.probe import probe_media
from videoslim.core.scanner import VideoScanner
from videoslim.platform.detection import platform_name
from videoslim.platform.ffmpeg_capabilities import (
    ffmpeg_available,
    ffmpeg_version,
    ffprobe_available,
    ffprobe_version,
    supported_encoders,
)
from videoslim.profiles.defaults import DEFAULT_PROFILES
from videoslim.profiles.loader import list_builtin_profiles, load_profile, validate_profile
from videoslim.profiles.schema import ProfileConfig

app = typer.Typer(help="VideoSlim command-line interface")
console = Console()

profile_app = typer.Typer(help="Manage built-in and custom profiles")
config_app = typer.Typer(help="View or initialize configuration")

app.add_typer(profile_app, name="profiles")
app.add_typer(config_app, name="config")


@app.command()
def scan(
    path: Annotated[
        Path,
        typer.Argument(exists=True, file_okay=False, readable=True, help="Directory to scan"),
    ],
    output: Annotated[
        Path | None,
        typer.Option(help="Output directory to avoid collisions"),
    ] = None,
    preset: Annotated[str, typer.Option(help="Named profile preset")] = "balanced",
) -> None:
    config = ScanConfig(input_dir=path, output_dir=output)
    files = VideoScanner().scan_directory(config)
    console.print(f"Discovered {len(files)} candidate video file(s) using preset '{preset}'.")
    for item in files[:20]:
        console.print(f"- {item.relative_path}")


@app.command()
def analyze(
    path: Annotated[
        Path,
        typer.Argument(exists=True, file_okay=False, readable=True, help="Directory to analyze"),
    ],
) -> None:
    config = ScanConfig(input_dir=path)
    files = VideoScanner().scan_directory(config)
    valid = 0
    invalid = 0
    console.print(f"Analyzing {len(files)} candidate file(s).")
    for item in files:
        result = probe_media(item.path)
        if result.is_valid_video:
            valid += 1
        else:
            invalid += 1
        if not result.is_valid_video:
            console.print(f"- {item.path.name}: no valid video stream ({'; '.join(result.warnings)})")
    console.print(f"Summary: {valid} valid video(s), {invalid} non-video or invalid file(s).")


@app.command()
def compress(
    path: Annotated[
        Path,
        typer.Argument(exists=True, file_okay=False, readable=True, help="Directory containing videos"),
    ],
    output: Annotated[
        Path | None,
        typer.Option(help="Directory for compressed outputs"),
    ] = None,
    profile: Annotated[str, typer.Option(help="Profile to use")] = "balanced",
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run/--no-dry-run", help="Preview the encoding plan without writing files"),
    ] = True,
) -> None:
    config = ScanConfig(input_dir=path, output_dir=output, scan_only=dry_run)
    files = VideoScanner().scan_directory(config)
    profile_config = ProfileConfig(**load_profile(profile))
    plan = build_plan(
        files,
        preset=profile,
        output_dir=output,
        container=profile_config.container or "mp4",
    )
    console.print(f"Prepared {len(plan)} task(s) using profile '{profile}'.")
    for item in plan[:20]:
        console.print(f"- {item['source']} -> {item['output']}")

    if dry_run:
        return
    if not ffmpeg_available():
        raise typer.BadParameter(
            "ffmpeg is not installed or not available on PATH; install FFmpeg before compressing.",
            param_hint="--no-dry-run",
        )

    audio_config = profile_config.audio
    audio_codec = audio_config.get("codec", "aac")
    if not isinstance(audio_codec, str):
        raise typer.BadParameter(f"Profile '{profile}' has an invalid audio codec.")

    crf = profile_config.crf if profile_config.crf is not None else 28
    for item in plan:
        encode_file(
            EncodeRequest(
                source=Path(str(item["source"])),
                destination=Path(str(item["output"])),
                preset=profile_config.preset,
                codec=profile_config.codec,
                crf=crf,
                cq=profile_config.cq,
                audio_codec=audio_codec,
                dry_run=False,
            )
        )
        console.print(f"Compressed {item['source']} -> {item['output']}")


@profile_app.command("list")
def list_profiles() -> None:
    for name in list_builtin_profiles():
        console.print(name)


@profile_app.command("show")
def show_profile(name: str) -> None:
    profile = load_profile(name)
    console.print(json.dumps(profile, indent=2, sort_keys=True))


@profile_app.command("validate")
def validate_profile_file(path: Annotated[Path, typer.Argument(exists=True, readable=True, help="Profile JSON file to validate")]) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    config = validate_profile(payload)
    console.print(f"Profile '{config.name}' is valid.")


@profile_app.command("import")
def import_profile(path: Annotated[Path, typer.Argument(exists=True, readable=True, help="Profile JSON file to import")]) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    config = validate_profile(payload)
    destination_dir = Path.home() / ".videoslim" / "profiles"
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{config.name}.json"
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    console.print(f"Imported profile '{config.name}' to {destination}.")


@profile_app.command("export")
def export_profile(name: str, output: Annotated[Path, typer.Option(help="File path for the exported profile")] = Path("./profile-export.json")) -> None:
    profile = load_profile(name)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(profile, indent=2), encoding="utf-8")
    console.print(f"Exported profile '{name}' to {output}.")


@config_app.command("init")
def init_config() -> None:
    config_path = default_config_path()
    save_default_config(config_path)
    console.print(f"Initialized configuration at {config_path}.")


@config_app.command("show")
def show_config() -> None:
    config = load_config(default_config_path())
    console.print(json.dumps(config.model_dump(mode="python"), indent=2, sort_keys=True))


@app.command()
def doctor() -> None:
    info = {
        "python_version": sys.version.split()[0],
        "platform": platform_name(),
        "ffmpeg_available": ffmpeg_available(),
        "ffprobe_available": ffprobe_available(),
        "ffmpeg_version": ffmpeg_version(),
        "ffprobe_version": ffprobe_version(),
        "supported_encoders": supported_encoders(),
        "builtin_profiles": list_builtin_profiles(),
    }
    console.print(json.dumps(info, indent=2, sort_keys=True))


@app.command()
def report(path: Annotated[Path, typer.Argument(help="Report file to create or read")]) -> None:
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "profiles": list(DEFAULT_PROFILES),
        "ffmpeg_available": ffmpeg_available(),
        "ffprobe_available": ffprobe_available(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    console.print(f"Wrote report to {path}.")


@app.command()
def version() -> None:
    console.print("VideoSlim 0.1.0")


if __name__ == "__main__":
    app()
