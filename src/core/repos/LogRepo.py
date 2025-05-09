from typing import List, Protocol
from src.core.models.GameLog import GameLog


class LogRepo(Protocol):
    def add_log(self, log: GameLog) -> None:
        """Add a log to the repository"""
        ...

    def get_logs(self) -> List[GameLog]:
        ...