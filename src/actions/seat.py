"""Seat customer action implementation"""

from dataclasses import dataclass
from typing import TypeVar
from pydantic import BaseModel, Field

from src.common.location import DINING
from src.core.entities.customer import CustomerStatus
from src.core.entities.seat import Seat
from src.core.models.Action import ActionResult, ValidationResult
from src.core.models.RestaurantState import RestaurantState

class SeatAction(BaseModel):
    """Take a seat"""
    customer_id: str = Field(description="The ID of the customer to seat")


    def is_valid(self, state: RestaurantState, employee_name: str) -> ValidationResult:
        
        if not customer_exists(state, self.customer_id):
            return ValidationResult(False, f"Customer {self.customer_id} does not exist.")
        if status(state, employee_name) != CustomerStatus.WAITING:
            return ValidationResult(False, f"Customer {self.customer_id} is not waiting.")
        
        return ValidationResult(True, None)

    def execute(self, state: RestaurantState, employee_name: str) -> ActionResult:
        seat = get_or_find_customer_seat(state, self.customer_id)
        step_toward_chair(state, self.customer_id, seat)

        if arrived_at_chair(state, self.customer_id, seat):
            return ActionResult(f"Customer {self.customer_id} is now seated at table.",  False)

        return ActionResult(f"{employee_name} is leading {self.customer_id} to a table.", True)


# Utilities --------------------------------
def get_or_find_customer_seat(state: RestaurantState, customer_id: str) -> Seat:
    seat = state.get_customer_seat_repo().get_customer_seat(customer_id)
    if seat:
        return seat

    seat = state.get_customer_seat_service().find_closest_seat_to_customer(customer_id)
    state.get_customer_seat_repo().set_customer_seat(customer_id, seat.seat_id)

    return seat

def step_toward_chair(state: RestaurantState, customer_id: str, seat: Seat):
    customer = state.get_customer_repo().get_customer(customer_id)
    path = state.get_navigation_service().get_path_between_positions(customer.position, seat.position)
    
    if path is None or len(path) == 0 or len(path) == 1:
        return ValueError("No path to the seat or already at the seat.")

    # Move the customer
    customer.position = path[1]
    state.get_customer_repo().update_customer(customer)

def arrived_at_chair(state: RestaurantState, customer_id: str, seat: Seat) -> bool:
    customer = state.get_customer_repo().get_customer(customer_id)
    return customer.position == seat.position

def customer_exists(state: RestaurantState, customer_id: str) -> bool:
    return state.get_customer_repo().get_customer(customer_id) is not None

def status(state: RestaurantState, customer_id: str) -> CustomerStatus:
    return state.get_customer_repo().get_customer(customer_id).status