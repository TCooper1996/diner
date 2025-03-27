from dataclasses import dataclass, field
import json
from typing import Dict, List, Optional, Tuple
from enum import Enum

from itertools import chain, cycle, groupby, zip_longest

from src.agents.models.Model import StandardMessage
from src.state.GameTurn import GameTurn
from src.state.employee.employee import Employee
from src.game_engine.location import *
from src.state.customer import Customer
from src.state.order import Order, OrderItem, OrderStatus
from src.state.restaurant_state import RestaurantState

@dataclass
class GameState:
    restaurant_state: RestaurantState
    employee_turns: List[GameTurn]
    tick: int = field(default=0)


    def employee_messages(self, name: str) -> List[StandardMessage]:
        employees_turns = [t.employees[name] for t in self.employee_turns]
        messages = []
        for turn in employees_turns:
            messages.extend(turn.get_messages())
        return messages

        
