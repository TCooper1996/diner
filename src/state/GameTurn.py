
from dataclasses import dataclass
from typing import List

from src.state.employee.EmployeeTurn import EmployeeTurn


@dataclass
class GameTurn:
    employees: List[EmployeeTurn]