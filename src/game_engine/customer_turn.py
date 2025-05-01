import copy
from src.core.entities.customer import *
from src.state.game_state.restaurant_state.restaurant_state import RestaurantState
from ..state.game_state import restaurant_state

class CustomerTurn:
    """Represents a turn for a customer, where they may perform actions like ordering food."""
    pass

def run_customer_update(r_state: RestaurantState, tick: int) -> CustomerTurn:
    # Check win/loss conditions
    if tick % 5 == 0 and len(r_state.customers) < 3:  # Add new customer every 5 ticks
        c = Customer()
        restaurant_state.add_customer(r_state, c, "entrance")
        
    # Update customer wait times and check for unhappy customers
    for c_id in r_state.customers.keys():
        update_customer(r_state, c_id)

    return CustomerTurn()

def update_customer(r_state: RestaurantState, customer_id: str) -> None:
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