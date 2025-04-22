
from dataclasses import dataclass
from typing import List

from src.common.position import Position


@dataclass
class EmployeeTurnInfo:
    employee_name: str
    action: str
    agent_messages: List[str]
    result: str


@dataclass
class EmployeeInfo:
    name: str
    position: Position
    instruction: str
    turns: List[EmployeeTurnInfo]