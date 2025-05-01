"""Notify kitchen of orders action implementation"""

from typing import List
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from src.actions.EmployeeActionInteractor import EmployeeActionInteractor
from src.actions.base import copy_args
from src.common.results import ActionResult, ActionResult, ValidationResult
from src.core.entities.order import OrderStatus


class SubmitOrdersToKitchen(BaseModel):
    """
    Notify kitchen of new orders
    """
    def is_valid(self, itr: EmployeeActionInteractor) -> ValidationResult:
        orders_taken = itr.get_orders_taken()
        orders_to_submit = [itr.get_order_status(o) for o in orders_taken if itr.get_order_status(o) == OrderStatus.PENDING]
        if len(orders_to_submit) == 0:
            return ValidationResult(False, f"{itr.employee_name} has no pending orders to submit to the kitchen.")
        return ValidationResult(True, None)
        

    def execute(self, itr: EmployeeActionInteractor) -> ActionResult:
        kitchen_id = itr.get_station_locked_by("kitchen", itr.employee_name)
        if kitchen_id is None:
            kitchen_id = itr.find_nearest_station("kitchen", itr.employee_name)
            itr.lock_station(kitchen_id, itr.employee_name)
        
        reached = itr.approach_entity(itr.employee_name, kitchen_id)
        if reached:
            submitted = itr.submit_orders()
            return ActionResult(f"Submitted {submitted} orders to kitchen", repeat=False)
        else:
            return ActionResult(f"{itr.employee_name} is leading orders to the kitchen at {kitchen_id}.", repeat=True)
            
