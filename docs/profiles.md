# Profiles

VideoSlim uses a validated JSON profile model. Built-in profiles are kept separate from user-created JSON configuration files and are loaded through the profile registry.

## Built-in profiles

- balanced: general-purpose compromise for everyday library compression.
- maximum_savings: stronger quality trade-off to reduce file size further.
- high_quality: conservative quality target with moderate file savings.
- fast_cpu: prioritizes quicker CPU-only encoding.
- nvidia_hevc: HEVC NVENC target when available.
- archive: conservative preservation profile for archive-style workflows.
- compatibility_h264: H.264 / MP4 compatibility profile.

## Validation and import

Custom profiles are validated before being accepted. Unknown fields are rejected, and only supported profile fields are allowed.
