from dataclasses import dataclass
from typing import List

from src.core.models.GameState import GameState


class GameUpdateEvent:
    def __init__(self, state: GameState):
        self.state = state.copy()
    
@dataclass
class NewGameEvent:
    update: GameUpdateEvent
