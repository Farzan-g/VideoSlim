# Compression profiles

A profile is a saved set of encoder choices. Select one by name with
`videoslim compress --profile NAME`. A profile does not promise a particular
output size: the result depends on the source video, the selected encoder,
and its settings.

## Built-in profiles

These are the profiles actually loaded by the CLI:

| Name | Video encoder | Encoder preset | Quality value | Output extension | Intended use |
| --- | --- | --- | --- | --- | --- |
| `balanced` | `libx264` (CPU, H.264) | `medium` | CRF 28 | `.mp4` | General-purpose starting point. |
| `maximum_savings` | `libx265` (CPU, HEVC) | `slower` | CRF 32 | `.mp4` | Smaller-file goal with a stronger quality trade-off and slower encoding. |
| `high_quality` | `libx264` (CPU, H.264) | `slow` | CRF 22 | `.mp4` | Higher visual quality target; results may be larger. |
| `fast_cpu` | `libx264` (CPU, H.264) | `veryfast` | CRF 30 | `.mp4` | Faster CPU encoding, usually less compression efficiency. |
| `nvidia_hevc` | `hevc_nvenc` (NVIDIA GPU, HEVC) | `p4` | CQ 28 | `.mp4` | NVIDIA hardware encoding when the driver and FFmpeg support it. |
| `archive` | `libx265` (CPU, HEVC) | `slow` | CRF 24 | `.mkv` | HEVC encoding with audio codec set to `copy`; not a bit-for-bit archive. |
| `compatibility_h264` | `libx264` (CPU, H.264) | `medium` | CRF 23 | `.mp4` | H.264 for broader playback compatibility. |

**CRF** means constant rate factor: a quality scale used by x264/x265, where a
lower number generally means higher quality and a larger file. **CQ** is
constant quality for NVENC and is a different encoder scale; do not compare
its number directly with CRF. The `preset` trades encoding speed for
compression efficiency; a slower preset does not itself mean lower quality.

Even profiles named “maximum savings” or “high quality” cannot guarantee a
size or visual result. To try a sample, put one video in a separate test
folder, run a preview for that folder, then encode it and compare the result
with the original.

## List, inspect, export, and validate

```powershell
videoslim profiles list
videoslim profiles show nvidia_hevc
videoslim profiles export nvidia_hevc --output ".\nvidia_hevc.json"
videoslim profiles validate ".\nvidia_hevc.json"
```

- `list` prints built-in profile names.
- `show NAME` prints the validated profile data for a built-in profile.
- `export NAME` writes built-in profile data to a JSON file. The default
  output, if `--output` is omitted, is `profile-export.json` in the current
  directory. Existing destination files can be overwritten.
- `validate PATH` parses a JSON object and validates it against the profile
  schema. Unknown top-level fields are rejected.

## Profile JSON fields

The schema accepts `id`, `name`, `label`, `description`, `version`,
`schema_version`, `codec`, `encoder`, `preset`, `crf`, `cq`,
`target_bitrate`, `max_bitrate`, `container`, `scale`, `audio`, `subtitles`,
`metadata`, `resolution`, `hardware`, and `fallback`. The `name` and `codec`
must not be blank; `crf` and `cq`, when present, must be between 0 and 63.
Nested settings are JSON objects.

The CLI currently applies only a subset when compressing: `codec`, `preset`,
`crf`, `cq`, `container`, and `audio.codec`. Other accepted fields—including
target bitrates, scaling/resolution, subtitle and metadata preservation,
hardware permissions, and fallback policy—are not applied by the current
encoder path. Do not assume that setting a field in profile JSON changes
compression.

## Import and custom profiles: incomplete

```text
videoslim profiles import PATH
```

The command validates a JSON file and copies it into the user's
`~/.videoslim/profiles` folder (on Windows:
`%USERPROFILE%\.videoslim\profiles`). However, the CLI does not pass this
folder to the profile loader. Consequently, an imported custom profile cannot
currently be selected by `compress` or inspected with `profiles show`.
`profiles list` lists built-in profiles only.

The checked-in JSON files in the repository's `profiles/` folder are not the
canonical profile definitions used by the CLI. For example,
`profiles/fast_cpu.json` says `faster` while the built-in profile uses
`veryfast`. `profiles/compatibility_h264.json` says CRF 25 (the built-in uses
23) and contains `pixel_format`, which the current schema rejects as an
unknown field. Use `profiles show` and `profiles export` for the actual
built-in values.

For a full list of which profile fields are applied and which codecs are
available, see [codecs and hardware acceleration](codecs.md).
