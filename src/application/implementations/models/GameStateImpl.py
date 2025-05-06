from dataclasses import dataclass

from src.core.models.GameState import GameState
from src.core.models.RestaurantState import RestaurantState
from src.core.repos.ActionRepo import ActionRepo
from src.core.repos.EmployeeMessageRepo import EmployeeMessageRepo


class GameStateImpl(GameState):
    restaurant_state: RestaurantState
    message_repo: EmployeeMessageRepo
    action_repo: ActionRepo
    tick: int

    def get_restaurant_state(self):
        return self.restaurant_state

    def get_message_repo(self) -> EmployeeMessageRepo:
        return self.message_repo

    def get_action_repo(self) -> ActionRepo:
        return self.action_repo

    def get_tick(self) -> int:
        return self.tick
    
    def copy(self) -> 'GameState':
        return GameStateImpl(
            restaurant_state=self.restaurant_state,
            message_repo=self.message_repo,
            action_repo=self.action_repo,
            tick=self.tick
        )