
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from src.actions import Action
from src.agents.models.Model import StandardMessage
from src.state.game_state.immutable_types.employee_turn import EmployeeTurn


@dataclass
class GameTurn:
    employees: List[EmployeeTurn] = field(default_factory=list)  # List of EmployeeTurn objects

    def get_employee_turn(self, name: str) -> None | EmployeeTurn:

        names =  [e.employee_name for e in self.employees]
        if name in names:
            return self.employees[names.index(name)]

        return None
        
    def get_actions(self) -> List[Tuple[str, Action]]:
        return [(turn.employee_name, turn.action) for turn in self.employees]

    def get_employee_messages(self, name: str) -> List[StandardMessage]:
        turn = self.get_employee_turn(name)
        if turn is None:
            return []
        return turn.get_messages()

    def add_turn(self, turn: EmployeeTurn):
        # Check if the employee already exists in the current turn
        existing_turn = self.get_employee_turn(turn.employee_name)
        if existing_turn is None:
            # If not, append the new turn to the employees list
            self.employees.append(turn)
        else:
            raise ValueError("Employee already has an entry")