from dataclasses import dataclass, field
import json
from typing import Dict, List, Optional, Tuple
from enum import Enum

from src.agents.models.Model import StandardMessage
from src.common.position import Position
from src.state.game_state.game_turn import GameTurn
from src.state.game_state.immutable_types.employee_turn import EmployeeTurn
from .restaurant_state import RestaurantState




@dataclass
class GameState:
    restaurant_state: RestaurantState
    turns: Dict[int, GameTurn] = field(default_factory=dict)
    tick: int = field(default=0)
    
    def last_game_turn(self) -> Optional[GameTurn]:
        if self.turns:
            return list(self.turns.values())[-1]
        return None

    def last_employee_turn(self) -> Optional[EmployeeTurn]:
        turn = self.last_game_turn()
        if turn is None or not turn.employees:
            return None
        return turn.employees[-1]


    def get_actions(self) -> List[Tuple[int, str, str]]:
        actions = []
        for i, turn in enumerate(self.turns.values()):
            actions.extend([(i, t[0], repr(t[1])) for t in turn.get_actions()])
        return actions

    def get_game_turns(self) -> List[GameTurn]:
        return list(self.turns.values())

    def get_employee_turns(self, name: str) -> List[EmployeeTurn]:
        maybe_turns =  map(lambda t: t.get_employee_turn(name), self.turns.values())
        filtered = filter(None, maybe_turns)  # Filter out None values
        return list(filtered)

    def employee_messages(self, name: str) -> List[StandardMessage]:
        employees_turns = self.get_employee_turns(name)
        messages = []
        for turn in employees_turns:
            messages.extend(turn.get_messages())
        return messages
