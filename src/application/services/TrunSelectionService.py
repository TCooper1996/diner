from dataclasses import dataclass, field
from typing import List
from src.actions import Action
from src.core.repos.ActionRepo import ActionRepo
from src.core.repos.CustomerRepo import CustomerRepo

# External
@dataclass
class EmployeeTurn:
    employee_id: str

@dataclass
class CustomerTurn:
    pass

# Internal classess
@dataclass
class EmployeeUpdate:
    index: int

class CustomerUpdate:
    pass

ActiveTurn = EmployeeUpdate | CustomerUpdate

@dataclass
class TurnSelectionService:    
    employee_ordering: List[str]
    active_turn: ActiveTurn = field(default=EmployeeUpdate(0))

    def choose_turn(self) -> EmployeeTurn | CustomerTurn:
        match (self.active_turn):
            case EmployeeUpdate(index=index):
                return EmployeeTurn(employee_id=self.employee_ordering[index])
            case CustomerUpdate():
                return CustomerTurn()
            case _:
                raise Exception("Invalid substate") 