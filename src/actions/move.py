"""Move action implementation"""

from typing import ClassVar, List, Literal
from pydantic import BaseModel, Field

from src.actions.EmployeeActionInteractor import EmployeeActionInteractor
from src.common.results import ActionResult, ActionResult, ValidationResult  # Updated import
from src.core.types import StationType, Stations


class MoveToNewRoom(BaseModel):
    """
    Tool for moving an employee to a different location
    """
    destination: StationType = Field(
        description=f"The location to move to. Options are {Stations}"
    )

    def is_valid(self, itr: EmployeeActionInteractor) -> ValidationResult:
        if itr.current_location() == self.destination:
            return ValidationResult(False, f"{itr.employee_name} is already at the {self.destination}.")
        
        if self.destination.lower() not in Stations:
            return ValidationResult(False, f"Cannot move to {self.destination}. Valid locations are: {', '.join(Stations)}")
        
        return ValidationResult(True, None)

    def execute(self, itr: EmployeeActionInteractor) -> ActionResult:
        current_location = itr.current_location()
        id = itr.find_station(self.destination)
        itr.lock_station(id, itr.employee_name)
        repeat = not itr.approach_entity(itr.employee_name, id)

        return ActionResult(f"{itr.employee_name} moved from {current_location} to {itr.current_location()}", repeat=repeat)
