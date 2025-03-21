"""
Actions package containing all available actions for the diner application.

Each action is contained in its own module and manages all aspects of that action:
- Action tool definition (used by the agent)
- Action implementation (business logic)
- Action state handling (updates to GameState)
"""

from typing import Dict, Literal, Union
from src.actions.base import ActionResult
from src.actions.move import *
from src.actions.pick_up_order import PickUpOrder
from src.actions.seat import *
from src.actions.take_order import *
from src.actions.notify_kitchen import *
from src.actions.cook import *
from src.actions.hand_order_to_customer import *
from src.actions.wait import *

# List of all action tools available to the agent
actionTypes = Literal[
    "move",
    "seat",
    "takeOrder",
    "cook",
    "deliver",
    "wait",
    "submitOrdersToKitchen"
]
EmployeeAction = Union[
    MoveToNewRoom,
    SeatAction, 
    TakeOrderAction,
    SubmitOrdersToKitchen,
    CookAction,
    HandOrderToCustomer,
    WaitAction
]

tools = {
    t.__name__:t for t in
    [MoveToNewRoom, 
     SeatAction, 
     TakeOrderAction,
     CookAction, 
     HandOrderToCustomer, 
     WaitAction, 
     SubmitOrdersToKitchen,
     PickUpOrder]
     }

    

def create_tools():
    """Create tool instances for each defined tool"""
    return list(tools.values())


def parse_tool(name, args) -> EmployeeAction:
    """Parse a tool invocation into an EmployeeAction"""
    t = tools[name]
    return t(**args)

