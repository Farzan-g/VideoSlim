from __future__ import annotations

from collections.abc import Iterable

from .models import JobSummary


def summarize_jobs(items: Iterable[dict[str, object]]) -> JobSummary:
    summary = JobSummary()
    for item in items:
        summary.files_discovered += 1
        summary.files_processed += 1
        raw_size = item.get("size_bytes", 0)
        size_bytes = int(raw_size) if isinstance(raw_size, int) else 0
        summary.total_input_bytes += size_bytes
    return summary
