import copy
from src.core.entities.customer import *
from .game_state import GameState
from . import restaurant_state

def update_customers(gamestate: GameState) -> GameState:
    gamestate = copy.deepcopy(gamestate)
    # Check win/loss conditions
    if gamestate.tick % 5 == 0 and len(gamestate.restaurant_state.customers) < 3:  # Add new customer every 5 ticks
        c = Customer()
        restaurant_state.add_customer(gamestate.restaurant_state, c, "entrance")
        
    # Update customer wait times and check for unhappy customers
    for c_id in gamestate.restaurant_state.customers.keys():
        update_customer(gamestate, c_id)

    return gamestate

def update_customer(gamestate: GameState, customer_id: str) -> None:
    r_state = gamestate.restaurant_state
    customer = r_state.grab_customer(customer_id)
    match customer.status:
        case CustomerStatus.EATING:
            customer.eating_time += 1
            if customer.eating_time >= 3:  # Assuming 3 ticks is the eating time limit
                customer.status = CustomerStatus.LEAVING
                station = r_state.station_manager.lookup_station_by_entity(customer_id)
                if station is None:
                    raise Exception(f"Customer {customer_id} is leaving but no station found for them.")
                r_state.station_manager.remove_entity_from_station(station, customer_id)
        case CustomerStatus.LEAVING:
            exit = r_state.station_manager.find_station("entrance")
            reached = r_state.location_manager.move_entity_toward( customer_id, exit)
            if reached :
                customer.status = CustomerStatus.DONE