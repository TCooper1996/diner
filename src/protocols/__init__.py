from typing import Protocol
from src.actions.EmployeeActionInteractor import EmployeeActionInteractor
from src.common.results import ActionResult, ValidationResult


class IAction(Protocol):
    def is_valid(self, itr: EmployeeActionInteractor) -> ValidationResult:
        ...
    def execute(self, itr: EmployeeActionInteractor) -> ActionResult:
        ...