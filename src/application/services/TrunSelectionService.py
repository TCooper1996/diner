from dataclasses import dataclass, field
from typing import List
from src.actions import Action
from src.core.models.ActiveTurn import *
from src.core.repos.ActionRepo import ActionRepo
from src.core.repos.CustomerRepo import CustomerRepo

@dataclass
class TurnSelectionService:    
    employee_ordering: List[str]

    def choose_turn(self, turn: ActiveTurn) -> ActiveTurn:
        match (turn):
            case EmployeeUpdate(name):
                next_index = self.employee_ordering.index(name) + 1
                if next_index == len(self.employee_ordering):
                    return CustomerUpdate()
                return EmployeeUpdate(self.employee_ordering[next_index])
            case CustomerUpdate():
                return EmployeeUpdate(self.employee_ordering[0])
            case _:
                raise Exception("Invalid substate") 