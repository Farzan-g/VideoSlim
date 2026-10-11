from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ProgressState:
    current: int = 0
    total: int = 0
    message: str = "Idle"
    warnings: list[str] = field(default_factory=list)

    def update(self, current: int, total: int | None = None, message: str | None = None) -> None:
        self.current = current
        if total is not None:
            self.total = total
        if message is not None:
            self.message = message
