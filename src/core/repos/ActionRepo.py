from dataclasses import dataclass
from typing import Protocol

from src.actions import Action


@dataclass
class ActionRepo(Protocol):
    def set_employee_action(self, employee_id: str, action: Action | None) -> None:
        """Set the action of an employee."""
        ...

    def get_employee_action(self, employee_id: str) -> Action | None:
        ...