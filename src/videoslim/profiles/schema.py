from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProfileConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str | None = None
    name: str = "balanced"
    label: str | None = None
    description: str = "General-purpose profile."
    version: int = 1
    schema_version: int = 1
    codec: str = "libx264"
    encoder: str = "cpu"
    preset: str = "medium"
    crf: int | None = Field(default=28, ge=0, le=63)
    cq: int | None = Field(default=None, ge=0, le=63)
    target_bitrate: str | None = None
    max_bitrate: str | None = None
    container: str | None = "mp4"
    scale: str | None = None
    audio: dict[str, Any] = Field(default_factory=dict)
    subtitles: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    resolution: dict[str, Any] = Field(default_factory=dict)
    hardware: dict[str, Any] = Field(default_factory=dict)
    fallback: dict[str, Any] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Profile name cannot be empty.")
        return cleaned

    @field_validator("codec")
    @classmethod
    def validate_codec(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Codec cannot be empty.")
        return value.strip()
