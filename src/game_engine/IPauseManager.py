from typing import Protocol


class IPauseManager(Protocol):
    def is_paused(self) -> bool:
        ...