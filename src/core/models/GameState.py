from dataclasses import dataclass
from typing import Protocol

from src.core.repos.ActionRepo import ActionRepo
from src.core.repos.EmployeeMessageRepo import EmployeeMessageRepo
from .RestaurantState import RestaurantState

@dataclass
class GameState(Protocol):
    def get_restaurant_state(self) -> RestaurantState:
        ...
    def get_message_repo(self) -> EmployeeMessageRepo:
        ...
    def get_action_repo(self) -> ActionRepo:
        ...
    def get_tick(self) -> int:
        ...

    def copy(self) -> "GameState":
        """
        Create a deep copy of the game state.
        This is used to ensure that the game state can be passed around without
        unintended side effects.
        """
        ...