"""Wait action implementation"""

from pydantic import BaseModel, Field
from langchain_core.tools import tool

from src.core.models.Action import ActionResult, ValidationResult
from src.core.models.RestaurantState import RestaurantState


class WaitAction(BaseModel):
    """
    Tool for waiting (taking no action)
    """

    def is_valid(self, state: RestaurantState, employee_id: str) -> ValidationResult:
        return ValidationResult(True, None)

    def execute(self, state: RestaurantState, employee_id: str) -> ActionResult:
        return ActionResult(f"{employee_id} is waiting for the next instruction.", repeat=False)
    

