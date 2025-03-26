"""Observe environment action implementation"""

import time
from src.actions.base import ActionResult
from src.state.game import GameState, OrderStatus
from src.state.employee.employee import Employee
from src.game_engine.location import DINING, ENTRANCE, KITCHEN

def observe_environment(employee: Employee, game_state: GameState) -> str:
    location = employee.location
    observation = f"{employee.name} looks around the {location}: "  
    
    if location == ENTRANCE:
        waiting_customers = game_state.get_waiting_customers()
        if waiting_customers:
            observation += f"There are {len(waiting_customers)} customers waiting to be seated."
        else:
            observation += "There are no customers waiting to be seated."

    elif location == DINING:
        # Get all customers in dining area
        dining_customers = [c for c in game_state.customers.values() 
                            if c.location == DINING]
        
        if not dining_customers:
            observation += "There are no customers in the dining area."
        else:
            for c in game_state.customers.values():
                observation += c.describe()

    elif location == KITCHEN:
        ready_to_cook = [o for o in game_state.orders.values()
        if o.status == OrderStatus.TAKEN]
        cooking_orders = [o for o in game_state.orders.values() 
                        if o.status == OrderStatus.COOKING]
        ready_orders = game_state.get_ready_orders()
        
        if not ready_to_cook and not cooking_orders and not ready_orders:
            observation += "There are no orders in the kitchen."
        else:
            if ready_to_cook:
                observation += f"There are {len(ready_to_cook)} orders waiting to be cooked. "
            if cooking_orders:
                observation += f"There are {len(cooking_orders)} orders being cooked. "
            if ready_orders:
                observation += f"There are {len(ready_orders)} orders ready to be delivered."
    return observation