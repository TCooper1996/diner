"""
Actions package containing all available actions for the diner application.

Each action is contained in its own module and manages all aspects of that action:
- Action tool definition (used by the agent)
- Action implementation (business logic)
- Action state handling (updates to GameState)
"""

from typing import Dict, Literal, Union
from src.actions.move import MoveToNewRoom
from src.actions.seat import SeatAction
from src.actions.take_order import TakeOrderAction
from src.actions.submit_orders_to_kitchen import SubmitOrdersToKitchen
from src.actions.cook import CookAction
from src.actions.deliver_order_to_customer import DeliverOrderToCustomer
from src.actions.wait import WaitAction
from src.actions.pick_up_order import PickUpOrder

# List of all action tools available to the agent
actionTypes = Literal[
    "seat",
    "takeOrder",
    "cook",
    "deliver",
    "wait",
    "submitOrdersToKitchen"
]
Action = Union[
    SeatAction, 
    TakeOrderAction,
    SubmitOrdersToKitchen,
    CookAction,
    DeliverOrderToCustomer,
    WaitAction,
    PickUpOrder
]

tools = {
    t.__name__:t for t in
     [SeatAction, 
     TakeOrderAction,
     CookAction, 
     DeliverOrderToCustomer, 
     WaitAction, 
     SubmitOrdersToKitchen,
     PickUpOrder]
     }

    

def create_tools():
    """Create tool instances for each defined tool"""
    return list(tools.values())


def parse_tool(name, args) -> Action:
    """Parse a tool invocation into an EmployeeAction"""
    t = tools[name]
    return t(**args)

