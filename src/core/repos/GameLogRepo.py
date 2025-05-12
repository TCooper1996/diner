from typing import List, Protocol

from src.core.models.Action import Action
from src.core.models.GameLog import GameLog


class GameLogRepo(Protocol):
    def get_game_logs(self) -> List[GameLog]:
        """Get the game log for a given game ID."""
        ...

    def add_choose_action_log(self, action: Action, response: str) -> None:
        """Set the game log for a given game ID."""
        ...

    def add_verify_action_log(self, action: Action, error_response: str | None) -> None:
        """Set the game log for a given game ID."""
        ...

    def add_execute_action_log(self, action: Action, state_result: str) -> None:
        """Set the game log for a given game ID."""
        ...
        