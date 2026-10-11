from __future__ import annotations

from .models import JobSummary


def format_summary(summary: JobSummary) -> str:
    return (
        f"Files discovered: {summary.files_discovered}\n"
        f"Files processed: {summary.files_processed}\n"
        f"Files skipped: {summary.files_skipped}\n"
        f"Input bytes: {summary.total_input_bytes}"
    )
