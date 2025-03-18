from typing import Dict, List, Any, Optional, Tuple
from src.game_engine.location import DINING, Location
from src.state.game import GameState, OrderStatus
from src.state.employee import Employee

"""
Ideally, this file should be the interface between the Agent and the gamestate.
Each of these functions should explicitly define any and all checks that need to be made
before an action can be taken.
Instead of directly modifying the GameState, these functions should just call the appropriate methods on the GameState
and return the result.
"""

class ActionResult:
    def __init__(self, success: bool, message: str, game_state: GameState):
        self.success = success
        self.message = message
        self.game_state = game_state
    
def move_to_location(employee: Employee, game_state: GameState, destination: str) -> ActionResult:
    """Move the employee to a different location in the restaurant"""
    current_location = employee.location
    if current_location == destination:
        return ActionResult(False, f"{employee.name} is already at the {destination}.", game_state)
    
    valid_locations = ["entrance", "dining", "kitchen"]
    if destination not in valid_locations:
        return ActionResult(False, f"Cannot move to {destination}. Valid locations are: {', '.join(valid_locations)}", game_state)
    
    # Update the employee's location in the game_state
    if employee.name in game_state.employees:
        game_state.employees[employee.name].location = destination
    
    return ActionResult(True, f"{employee.name} moved from the {current_location} to the {destination}.", game_state)

def seat_customer(employee: Employee, game_state: GameState) -> ActionResult:
    """Seat a waiting customer from the entrance to the dining area"""
    if employee.location != "entrance":
        return ActionResult(False, f"{employee.name} cannot seat customers from the {employee.location}. You need to be at the entrance.", game_state)
    
    # Find waiting customers at the entrance
    waiting_customers = game_state.get_waiting_customers()
    
    if not waiting_customers:
        return ActionResult(False, f"There are no waiting customers at the entrance for {employee.name} to seat.", game_state)
    
    # Take the first waiting customer
    customer = waiting_customers[0]
    customer_id = customer.id
    
    # Update the customer's state using the GameState method
    if game_state.seat_customer(customer_id):
        return ActionResult(True, f"{employee.name} seated customer {customer.name} at a table in the dining area.", game_state)
    else:
        return ActionResult(False, f"Something went wrong. Customer {customer.name} could not be seated.", game_state)

def take_order(employee: Employee, game_state: GameState) -> ActionResult:
    """Take an order from a seated customer"""
    if employee.location != "dining":
        return ActionResult(False, f"{employee.name} cannot take orders from the {employee.location}. You need to be in the dining area.", game_state)
    
    # Find seated customers in the dining area
    seated_customers = game_state.get_seated_customers()
    
    if not seated_customers:
        return ActionResult(False, f"There are no seated customers ready to order for {employee.name} to help.", game_state)
    
    # Take the first seated customer
    customer = seated_customers[0]
    customer_id = customer.id
    
    # Use GameState method to take order
    items = game_state.take_customer_order(customer_id, employee.name)
    
    if items:
        return ActionResult(True, f"{employee.name} took an order from customer {customer.name} for {', '.join(items)}. The order needs to be brought to the kitchen.", game_state)
    else:
        return ActionResult(False, f"Something went wrong. Could not take order from customer {customer.name}.", game_state)

def notify_kitchen_of_orders(employee: Employee, game_state: GameState) -> ActionResult:
    """Register orders so they can be cooked"""
    if employee.location != "kitchen":
        return ActionResult(False, f"{employee.name} cannot notify the kitchen from the {employee.location}. You need to be in the kitchen.", game_state)
    
    # Find orders that need to be cooked
    orders = [order.id for order in game_state.orders.values() if order.status == OrderStatus.PENDING and order.server == employee.name]
    game_state.submit_orders_to_kitchen(orders)
    
    
    return ActionResult(True, f"Submitted {len(orders)} orders to kitchen", game_state)

def cook_food(employee: Employee, game_state: GameState, order_id: str) -> ActionResult:
    """Cook food for a pending order"""
    if employee.location != "kitchen":
        return ActionResult(False, f"{employee.name} cannot cook food from the {employee.location}. You need to be in the kitchen.", game_state)
    
    order = game_state.orders[order_id]
    if order_id and game_state.cook_order(order_id):
        return ActionResult(True, f"{employee.name} prepared order #{order_id}: {order.items}.", game_state)
    else:
        return ActionResult(False, f"Something went wrong. Could not prepare order #{order_id}.", game_state)

def deliver_food(employee: Employee, game_state: GameState) -> ActionResult:
    """Deliver cooked food to a customer"""
    if employee.location != "dining":
        return ActionResult(False, f"{employee.name} cannot deliver food from the {employee.location}. You must be in the dining room.", game_state)
    
    # Find orders that are ready to be delivered
    ready_orders = game_state.get_ready_orders()
    
    if not ready_orders:
        return ActionResult(False, f"There is no food ready for {employee.name} to deliver.", game_state)
    
    # Take the first ready order
    order = ready_orders[0]
    customer_id = order.customer_id
    items = order.items
    
    # Find the order ID
    order_id = None
    for oid, o in game_state.orders.items():
        if o.customer_id == customer_id and o.status == OrderStatus.READY:
            order_id = oid
            break
    
    if order_id and game_state.deliver_order(order_id):
        return ActionResult(True, f"{employee.name} delivered {', '.join(items)} to customer {customer_id}. The customer is now eating.", game_state)
    else:
        return ActionResult(False, f"Something went wrong. Could not deliver order to customer {customer_id}.", game_state)

def observe_environment(employee: Employee, game_state: GameState) -> ActionResult:
    """Look around the current location and report what is seen"""
    location = employee.location
    observation = f"{employee.name} looks around the {location}. "  
    
    if location == "entrance":
        waiting_customers = game_state.get_waiting_customers()
        if waiting_customers:
            observation += f"There are {len(waiting_customers)} customers waiting to be seated."
        else:
            observation += "There are no customers waiting to be seated."
    
    elif location == "dining":
        # Get all customers in dining area
        dining_customers = [c for c in game_state.customers.values() 
                            if c.location == DINING]
        
        if not dining_customers:
            observation += "There are no customers in the dining area."
        else:
            waiting_for_order = [c for c in dining_customers if c.status == "seated"]
            waiting_for_food = [c for c in dining_customers if c.status == "ordered"]
            eating = [c for c in dining_customers if c.status == "eating"]
            
            if waiting_for_order:
                observation += f"There are {len(waiting_for_order)} customers waiting to place orders. "
            if waiting_for_food:
                observation += f"There are {len(waiting_for_food)} customers waiting for their food. "
            if eating:
                observation += f"There are {len(eating)} customers eating their food."
    
    elif location == "kitchen":
        pending_orders = game_state.get_pending_orders()
        cooking_orders = [o for o in game_state.orders.values() 
                        if o.status == OrderStatus.COOKING]
        ready_orders = game_state.get_ready_orders()
        
        if not pending_orders and not cooking_orders and not ready_orders:
            observation += "There are no orders in the kitchen."
        else:
            if pending_orders:
                observation += f"There are {len(pending_orders)} orders waiting to be cooked. "
            if cooking_orders:
                observation += f"There are {len(cooking_orders)} orders being cooked. "
            if ready_orders:
                observation += f"There are {len(ready_orders)} orders ready to be delivered."
    
    return ActionResult(True, observation, game_state)