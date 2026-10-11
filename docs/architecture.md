# Architecture

VideoSlim is organized as a headless core plus a CLI surface. The core contains scanner, planner, encoding, and verification modules, while the CLI layer formats and exposes commands.

## Layers

- CLI: Typer commands and output rendering
- Core: scan, plan, encode, verify, and manage jobs
- Profiles: preset definitions and profile loading
- Platform: capability detection and FFmpeg runtime checks
- Config: user settings and path resolution
