
import json
from typing import List
from src.core.models.RestaurantState import RestaurantState


def to_prompt(state: RestaurantState) -> str:
    orders = state.get_order_repo().get_all_orders()
    employees = state.get_employee_repo().get_all_employees()
    customers = state.get_customer_repo().get_all_customers()
    customer_orders = state.get_customer_order_repo()
    employee_orders = state.get_employee_order_repo()
    employee_dict = {}


    for e in employees:
        orders_taken = employee_orders.get_orders_taken(e.name)
        orders_being_carried = employee_orders.get_orders_carried(e.name)
        employee_dict[e.name] = {
            "name": e.name,
            "orders_taken": orders_taken,
            "orders_being_carried": orders_being_carried,
        }

    customer_dict = {}
    for c in customers:
        customer_dict[c.name] = {
            "name": c.name,
            "status": c.status.value,
            "orders": repr(customer_orders.get_order_of_customer(c.name)),
        }

    d = {
        "employees": employee_dict,
        "customers": customer_dict,
        "orders": {f"#{o.id}": {"status": o.status.value, "order#": o.id} for o in orders},
    }
    return json.dumps(d, indent=4)