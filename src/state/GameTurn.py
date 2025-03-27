
from dataclasses import dataclass
from typing import Dict, List

from src.agents.models.Model import StandardMessage
from src.state.employee.EmployeeTurn import EmployeeTurn


@dataclass
class GameTurn:
    employees: Dict[str, EmployeeTurn]

    def get_employee_messages(self, name: str) -> List[StandardMessage]:
        return self.employees[name].get_messages()