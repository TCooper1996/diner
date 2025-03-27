# Persistent state for an employee that remains between ticks
from dataclasses import dataclass, field
from typing import Any, List, TYPE_CHECKING, Tuple
from langchain_core.messages import BaseMessage


from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.game_engine.location import ENTRANCE, Location
from src.protocols import IAction
from src.state.employee.EmployeeTurn import EmployeeTurn
from src.state.employee.EmployeeDecision import EmployeeDecision
from src.state.employee_state import EmployeeState

@dataclass
class Employee:
    name: str
    instruction: str
    location: Location
    current_action: IAction
