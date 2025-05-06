from dataclasses import dataclass
from typing import Optional, Protocol

from src.core.models.RestaurantState import RestaurantState

@dataclass
class ActionResult:
    message: str
    repeat: bool = False


@dataclass
class ValidationResult:
    success: bool
    error_msg: Optional[str] = None

class Action(Protocol):
    def verify(self, state: RestaurantState, employee_id: str) -> ValidationResult:
        """Verify if the action is valid in the current state"""
        ...
    def execute(self, state: RestaurantState, employee_id: str) -> ActionResult:
        ...