"""Notify kitchen of orders action implementation"""

from functools import reduce
from typing import List
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from src.actions.base import copy_args
from src.core.entities.grill import Grill
from src.core.entities.order import Order, OrderStatus
from src.core.models.Action import ActionResult, ValidationResult
from src.core.models.RestaurantState import RestaurantState


class SubmitOrdersToKitchen(BaseModel):
    """
    Notify kitchen of new orders
    """
    def is_valid(self, state: RestaurantState, employee_id: str) -> ValidationResult:
        if len(get_orders_to_submit(state, employee_id)) == 0:
            return ValidationResult(False, f"{employee_id} has no pending orders to submit to the kitchen.")
        return ValidationResult(True, None)
        

    def execute(self, state: RestaurantState, employee_id: str) -> ActionResult:
        grill_id = state.get_employee_grill(employee_id)
        if grill_id is None:
            grill = find_nearest_unoccupied_grill(state, employee_id)
            state.set_employee_grill(employee_id, grill.grill_id)
        else:
            grill = state.get_grill(grill_id)

        step_toward_grill(state, employee_id, grill)

        if grill_reached(state, employee_id, grill):
            submit_orders(state, employee_id)
            return ActionResult(f"Submitted {len(get_orders_to_submit(state, employee_id))} orders to kitchen", repeat=False)
        else:
            return ActionResult(f"{employee_id} is bringing orders to the kitchen at.", repeat=True)
            

# Utilities --------------------------------
def get_orders_to_submit(state: RestaurantState, employee_name: str) -> List[Order]:
    # Get orders taken which have not been submitted yet
    orders_taken = [state.get_order(o) for o in state.get_orders_taken(employee_name)]
    # Filter out orders that are not pending
    orders_to_submit = [o for o in orders_taken if o.status == OrderStatus.PENDING]
    return orders_to_submit

def find_nearest_unoccupied_grill(state: RestaurantState, employee_name: str) -> Grill:
    all_grills = state.get_all_grills()
    unoccupied_grills = [g for g in all_grills if not state.is_grill_occupied(g.grill_id)]
    if not unoccupied_grills:
        raise ValueError("No unoccupied grills available.")
    # Find closest one
    employee_position = state.get_employee(employee_name).position
    path_lengths = [len(state.get_navigation_service().get_path_between_positions(employee_position, g.position)) for g in  unoccupied_grills]
    nearest_grill_path = reduce(lambda closest_grill_path, grill_path: closest_grill_path if closest_grill_path[1] < grill_path[1] else grill_path, zip(unoccupied_grills, path_lengths))

    return nearest_grill_path[0]


def step_toward_grill(state: RestaurantState, employee_name: str, grill: Grill):
    employee = state.get_employee(employee_name)
    path = state.get_navigation_service().get_path_between_positions(employee.position, grill.position)
    
    if path is None or len(path) == 0 or len(path) == 1:
        return ValueError("No path to the seat or already at the seat.")

    # Move the customer
    employee.position = path[1]
    state.update_employee(employee)

def grill_reached(state: RestaurantState, employee_name: str, grill: Grill) -> bool:
    employee = state.get_employee(employee_name)
    return employee.position == grill.position

def submit_orders(state: RestaurantState, employee_name: str) -> int:
    """Submit orders to kitchen. Only need to update order repo."""
    orders = get_orders_to_submit(state, employee_name)
    for order in orders:
        order.status = OrderStatus.SUBMITTED
        state.update_order(order)
    return len(orders)