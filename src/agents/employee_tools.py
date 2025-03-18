from typing import Dict, List, Any, Optional, Callable, Tuple, TypedDict, Type, Literal, Union
from pydantic import  BaseModel, Field
from langchain_core.tools import tool, BaseTool
from src.game_engine import location

actions = Literal["move", "seat", "takeOrder", "cook", "deliver", "wait", "notifyKitchenOfOrders"]

# Base class for all tool classes to share common properties
class ToolBase(BaseModel):
    """Base class for all tool classes with common attributes"""
    action: str  # All tools have an action field
    
    @classmethod
    def get_action_type(cls) -> str:
        """Get the action type for this tool class"""
        # This would return the default value for the action field
        return cls.model_fields["action"].default
        
    @staticmethod
    def from_action(action_obj: 'EmployeeAction') -> str:
        """Extract the action type from any tool object"""
        return action_obj.action

# Tool schemas for employee actions
class MoveTool(ToolBase):
    # Use string instead of Literal to avoid serialization issues
    destination: str = Field(
        description="The location to move to (entrance, dining, or kitchen)"
    )
    action: str = Field(default="move")
@tool
def move_tool(destination: str):
    """Move the employee to a specific location in the restaurant"""
    # Validate destination
    valid_destinations = ["entrance", "dining", "kitchen"]
    if destination not in valid_destinations:
        raise ValueError(f"Invalid destination: {destination}. Must be one of: {valid_destinations}")
    return MoveTool(destination=destination)


class SeatTool(ToolBase):
    action: str = Field(default="seat")
    pass

@tool
def seat_customer_tool():
    """Seat a waiting customer (must be at entrance with waiting customers)"""
    return SeatTool()


class TakeOrderTool(ToolBase):
    action: str = Field(default="takeOrder")
    pass

@tool
def take_order_tool():
    """Take a customer's order (must be at dining with seated customers)"""
    return TakeOrderTool()

class NotifyKitchenOfOrdersTool(ToolBase):
    action: str = Field(default="notifyKitchenOfOrders")
    pass

@tool
def notify_kitchen_of_orders_tool():
    """Notify kitchen of new orders (must be at kitchen with orders to send)"""
    return NotifyKitchenOfOrdersTool()

class CookTool(ToolBase):
    action: str = Field(default="cook")
    order_id: str = Field(
        description="The ID of the order to cook"
    )
    pass

@tool
def cook_tool(order_id: str):
    """Cook food for a 'TAKEN' order (must be at kitchen with 'TAKEN' orders)
    (An order is 'PENDING' when it is taken from the customer. It becomes 'TAKEN' when it is brought to the kitchen)
    """
    return CookTool(order_id=order_id)


class DeliverTool(ToolBase):
    action: str = Field(default="deliver")
    pass

@tool
def deliver_tool():
    """Hand food to a customer (You must be at dining with seated customers)"""
    return DeliverTool()



class WaitTool(ToolBase):
    action: str = Field(default="wait")
    pass

@tool
def wait_tool():
    """Wait and take no action"""
    return WaitTool()



# Define a union type for all tool classes
EmployeeAction = Union[
    MoveTool,
    SeatTool, 
    TakeOrderTool,
    NotifyKitchenOfOrdersTool,
    CookTool,
    DeliverTool,
    WaitTool
]

tools = {
    "move": move_tool, "seat": seat_customer_tool, 
    "takeOrder": take_order_tool, "cook": cook_tool, 
    "deliver": deliver_tool, "wait": wait_tool,
    "notifyKitchenOfOrders": notify_kitchen_of_orders_tool}
def lookup_tool(name) -> BaseTool:
    """Lookup a tool by name"""
    for tool in tools.values():
        if tool.name == name:
            return tool
    raise ValueError(f"Tool {name} not found")

def create_tools():
    """Create tool instances for each defined tool"""
    return list(tools.values())

def parse_tool(name, args) -> EmployeeAction:
    f = lookup_tool(name)
    if f is None:
        raise ValueError(f"Tool {name} not found")
    return f.invoke(args)
