"""Wait action implementation"""

from pydantic import BaseModel, Field
from langchain_core.tools import tool

from src.actions.EmployeeActionInteractor import EmployeeActionInteractor
from src.common.results import ActionResult, ActionResult, ValidationResult


class WaitAction(BaseModel):
    """
    Tool for waiting (taking no action)
    """

    def is_valid(self, itr: EmployeeActionInteractor) -> ValidationResult:
        return ValidationResult(True, None)

    def execute(self, itr: EmployeeActionInteractor) -> ActionResult:
        return ActionResult(f"{itr.employee_name} is waiting for the next instruction.")
    

