from typing import Protocol

from src.core.models.ActiveTurn import ActiveTurn
from src.core.repos.ActionRepo import ActionRepo
from src.core.repos.EmployeeMessageRepo import EmployeeMessageRepo
from src.core.services.AgentService import AgentService
from .RestaurantState import RestaurantState

class GameState(ActionRepo, EmployeeMessageRepo, AgentService, RestaurantState, Protocol):
    def get_tick(self) -> int:
        ...

    def get_whose_turn(self) -> ActiveTurn:
        """
        Get the current player's turn.
        This is used to determine which player's turn it is in a multiplayer game.
        """
        ...

    def set_whose_turn(self, player_id: ActiveTurn) -> None:
        """
        Set the current player's turn.
        This is used to determine which player's turn it is in a multiplayer game.
        """
        ...

    def copy(self) -> "GameState":
        """
        Create a deep copy of the game state.
        This is used to ensure that the game state can be passed around without
        unintended side effects.
        """
        ...