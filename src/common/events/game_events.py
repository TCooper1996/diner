from dataclasses import dataclass
from typing import List

from src.core.models.GameState import GameState


@dataclass
class GameUpdateEvent:
    state: GameState
    def __post_init__(self):
        self.state = self.state.copy()
    
@dataclass
class NewGameEvent:
    update: GameUpdateEvent
