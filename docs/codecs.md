# Codecs and hardware acceleration

A **codec** is the method used to store video or audio. An **encoder** is the
software or hardware that applies that method. A **container** is the file
format holding the video and audio streams, such as MP4 or MKV. FFmpeg is the
program VideoSlim uses to create the output.

## Encoders listed by VideoSlim

VideoSlim recognizes these names when reading FFmpeg's encoder list:

| Encoder name | Meaning |
| --- | --- |
| `libx264` | CPU H.264 video encoding. |
| `libx265` | CPU HEVC/H.265 video encoding. |
| `libsvtav1` | CPU SVT-AV1 video encoding. |
| `libaom-av1` | CPU AV1 video encoding. |
| `h264_nvenc`, `hevc_nvenc` | NVIDIA GPU H.264 and HEVC video encoding. |
| `h264_qsv`, `hevc_qsv` | Intel Quick Sync Video H.264 and HEVC encoding. |
| `h264_amf`, `hevc_amf` | AMD AMF H.264 and HEVC encoding. |
| `copy` | Passes an encoded stream through without re-encoding it. |

The `doctor` command asks FFmpeg for its encoder list when FFmpeg is found.
When FFmpeg is missing, VideoSlim returns its built-in list of recognized
names; those names are **not** proof that the encoders are installed.

Only the built-in profile choices are wired to compression today: `libx264`,
`libx265`, and `hevc_nvenc`. The other names do not have selectable built-in
profiles or a custom-profile workflow that can be used by the CLI.

An internal hardware-profile catalog also names `av1_nvenc`, `av1_qsv`,
`h264_videotoolbox`, and `hevc_videotoolbox`. These are metadata only: they
are not included in the runtime encoder list and cannot be selected by the
CLI.

## CPU and GPU encoding

CPU profiles use x264 or x265. CPU encoding is broadly available but can be
slow, especially with `slow` or `slower` presets.

The `nvidia_hevc` profile selects `hevc_nvenc`, the NVIDIA hardware HEVC
encoder. It uses the `p4` preset and CQ value 28. To use it, all of these must
be true:

1. The computer has a supported NVIDIA GPU.
2. The NVIDIA driver is installed and working.
3. The FFmpeg program found on PATH was built with `hevc_nvenc`.
4. FFmpeg can initialize NVENC with that GPU and driver.

`videoslim doctor` checks whether FFmpeg lists `hevc_nvenc`. It cannot prove
that an actual encode will initialize; the encode itself is the definitive
test.

VideoSlim does not currently select Intel Quick Sync or AMD AMF through a
built-in profile. It does not automatically detect the GPU model or implement
the fallback policies described in profile data. If NVENC fails, compression
stops with FFmpeg's error; there is no automatic CPU retry.

## Quality and speed controls

- **CRF** is used by the CPU H.264/HEVC profiles. Within the same codec and
  general context, lower values usually preserve more detail and create larger
  files; higher values usually create smaller files with more visible quality
  loss.
- **CQ** is used by the NVENC profile. It is not numerically equivalent to
  CRF.
- **Preset** controls encoder speed/compression trade-offs. Preset names and
  behavior depend on the encoder. The CPU profiles use `medium`, `slow`,
  `slower`, or `veryfast`; NVENC uses `p4`.
- File size is content-dependent. A profile name is not a promise that every
  output will be smaller.

## Audio, subtitles, metadata, and resolution

The active encode command sets a video codec, preset, quality value, and one
audio codec. Most built-in profiles set audio to AAC; `archive` sets its audio
codec to `copy`. The current command does not implement the other profile
claims about preserving all audio tracks, copying subtitles, preserving
metadata, or enforcing resolution limits. It also does not expose an
`--audio`, `--subtitle`, `--resolution`, or codec command-line option.

FFmpeg applies its default stream selection for input files. If all tracks,
subtitles, or metadata are important, inspect the result carefully before
deleting or moving the source. Support for those profile fields is incomplete.

For the exact built-in settings and their intended use, see
[compression profiles](profiles.md).
