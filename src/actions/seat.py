"""Seat customer action implementation"""

from dataclasses import dataclass
from typing import TypeVar
from pydantic import BaseModel, Field

from src.actions.EmployeeActionInteractor import EmployeeActionInteractor
from src.common.location import DINING
from src.common.results import ActionResult, ActionResult, ValidationResult  # Updated import
from src.core.entities.customer import CustomerStatus


class SeatAction(BaseModel):
    """Take a seat"""
    customer_id: str = Field(description="The ID of the customer to seat")


    def is_valid(self, e: EmployeeActionInteractor) -> ValidationResult:
        
        if not e.customer_exists(self.customer_id):
            return ValidationResult(False, f"Customer {self.customer_id} does not exist.")
        if e.customer_status(self.customer_id) != CustomerStatus.WAITING:
            return ValidationResult(False, f"Customer {self.customer_id} is not waiting.")
        
        return ValidationResult(True, None)

    def execute(self, e: EmployeeActionInteractor) -> ActionResult:
        seat_id = e.get_station_locked_by("dining", self.customer_id)
        if seat_id is None:
            seat_id = e.find_nearest_station("dining", self.customer_id)
            e.lock_station(seat_id, self.customer_id)

        reached = e.approach_entity(self.customer_id, seat_id)
        e.approach_entity(e.employee_name, self.customer_id)
        
        if reached:
            e.set_customer_status(self.customer_id, CustomerStatus.SEATED)  # Update the customer's status to SEATED
            return ActionResult(f"Customer {self.customer_id} is now seated at table {seat_id}.",  repeat=False)

        return ActionResult(f"{e.employee_name} is leading {self.customer_id} to table {seat_id}.", repeat=True)