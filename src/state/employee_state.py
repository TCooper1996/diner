from dataclasses import dataclass
from typing import List
from src.game_engine.location import Location
from src.state.employee.EmployeeTurn import EmployeeTurn

@dataclass 
class EmployeeState:
    location:Location
    turns: List[EmployeeTurn]

    def add_turn(self, turn: EmployeeTurn):
        self.turns.append(turn)
