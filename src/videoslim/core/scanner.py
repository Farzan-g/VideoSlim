from __future__ import annotations

import fnmatch
import os
from pathlib import Path

from .models import ScanConfig, VideoFile
from .probe import probe_media


class VideoScanner:
    """Discover candidate video files in a directory tree."""

    def __init__(self, extensions: set[str] | None = None) -> None:
        self.video_extensions = set(extensions or {
            ".mp4",
            ".mkv",
            ".mov",
            ".avi",
            ".webm",
            ".m4v",
            ".mpg",
            ".mpeg",
            ".ts",
            ".mts",
            ".m2ts",
            ".wmv",
            ".flv",
            ".3gp",
        })

    def is_video_hint(self, path: Path) -> bool:
        return path.suffix.lower() in self.video_extensions

    def relative_output_path(self, file_path: Path, input_dir: Path, output_dir: Path | None) -> Path:
        relative = file_path.relative_to(input_dir)
        if output_dir is None:
            return relative
        return output_dir / relative

    def _matches_exclude(self, path: Path, patterns: tuple[str, ...]) -> bool:
        if not patterns:
            return False
        path_str = str(path).replace("\\", "/")
        return any(fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path.name, pattern) for pattern in patterns)

    def scan_directory(self, config: ScanConfig) -> list[VideoFile]:
        if config.output_overlaps_input():
            raise ValueError("The output directory overlaps with the input directory and would recurse into source files.")

        input_dir = config.input_dir.resolve()
        results: list[VideoFile] = []
        seen: set[Path] = set()

        for root, dirs, files in os.walk(input_dir, topdown=True, followlinks=config.follow_symlinks):
            root_path = Path(root)
            dirs[:] = [
                d for d in dirs
                if not (root_path / d).is_symlink() or config.follow_symlinks
            ]

            for directory_name in list(dirs):
                dir_path = root_path / directory_name
                if not config.include_hidden and dir_path.name.startswith("."):
                    dirs.remove(directory_name)
                    continue
                if self._matches_exclude(dir_path, config.exclude_globs):
                    dirs.remove(directory_name)
                    continue

            for file_name in sorted(files):
                file_path = root_path / file_name
                resolved = file_path.resolve(strict=False)
                if resolved in seen:
                    continue
                seen.add(resolved)
                if not config.include_hidden and file_name.startswith("."):
                    continue
                if self._matches_exclude(file_path, config.exclude_globs):
                    continue
                if file_path.is_symlink() and not config.follow_symlinks:
                    continue
                if not file_path.is_file():
                    continue
                if not self.is_video_hint(file_path):
                    continue

                try:
                    file_size = file_path.stat().st_size
                except OSError:
                    continue

                if config.min_size_bytes is not None and file_size < config.min_size_bytes:
                    continue
                if config.max_size_bytes is not None and file_size > config.max_size_bytes:
                    continue

                relative_path = file_path.relative_to(input_dir)
                candidate = VideoFile(
                    path=file_path,
                    relative_path=relative_path,
                    file_size=file_size,
                    extension=file_path.suffix.lower(),
                    discovered_by_hint=True,
                    is_valid_video=False,
                )
                probe = probe_media(file_path)
                candidate.is_valid_video = probe.is_valid_video
                candidate.probe_summary = {
                    "container": probe.container,
                    "duration": probe.duration,
                    "video_stream_count": len(probe.video_streams),
                    "audio_stream_count": len(probe.audio_streams),
                    "subtitle_stream_count": len(probe.subtitle_streams),
                    "ffprobe_available": probe.ffprobe_available,
                    "warnings": probe.warnings,
                }
                if probe.is_valid_video:
                    results.append(candidate)

        return results
