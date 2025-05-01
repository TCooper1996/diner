import copy
from typing import List, Literal
from src.common.location import Location
from src.common.position import Position
from src.core.types import StationType, TileType
from src.core.entities.customer import CustomerStatus
from src.core.entities.order import Order, OrderStatus

from src.state.game_state.restaurant_state import closest_station, RestaurantState
from src.actions.EmployeeActionInteractor import EmployeeActionInteractor as IEmployeeActionInteractor


SpawnLocation = Literal["entrance", "dining", "kitchen"]


class EmployeeActionInteractor(IEmployeeActionInteractor):
    def __init__(self, restaurant_state: RestaurantState, employee_name: str):
        self.restaurant_state = restaurant_state
        self.location_manager = self.restaurant_state.location_manager
        self.station_manager = self.restaurant_state.station_manager  # Assuming the location manager handles station locations
        self.name = employee_name

    @property
    def employee_name(self) -> str:
        return self.name

    def get_station_locked_by(self, station_type, entity_id):
        return self.station_manager.lookup_station_by_entity(entity_id)

    def find_nearest_station(self, station_type, entity_id):
        return closest_station(entity_id, self.station_manager, self.location_manager, station_type)

    def submit_orders(self) -> int:
        orders: List[str] = self.restaurant_state.orders_taken_by_employee(self.employee_name)
        submitted = 0
        for o in orders:
            submitted += 1
            self.set_order_status(o, OrderStatus.SUBMITTED)  # Update the order status in the restaurant state
        return submitted

    def add_order_to_inventory(self, order_id):
        orders = self.restaurant_state.order_carriers.get(self.employee_name, [])
        self.restaurant_state.order_carriers[self.employee_name] = [*orders, order_id]  # Ensure the entry exists

    def remove_order_from_inventory(self, order_id):
        return self.restaurant_state.order_carriers[self.employee_name].remove(order_id)

    def order_exists(self, order_id: str) -> bool:
        return self.restaurant_state.order_manager.get_order(order_id) is not None

    def get_order_status(self, order_id) -> OrderStatus:
        return self.restaurant_state.order_manager.grab_order(order_id).status

    def cook_order(self, order_id: str) -> bool:
        """
        Cook the order, returns True if the order is finished cooking, otherwise False.
        """
        return True    
    
    def set_order_status(self, order_id, status):
        self.restaurant_state.update_order_status(order_id, status)  # Update the order status in the restaurant state

    def get_orders_carried(self) -> list[str]:
        return self.restaurant_state.orders_carried_by_employee(self.employee_name)  # Get the list of orders carried by the employee

    def get_orders_taken(self) -> list[str]:
        return self.restaurant_state.orders_taken_by_employee(self.employee_name)  # Get the list of orders taken by the employee

    def get_ready_orders(self) -> List[str]:
        return [o.id for o in self.restaurant_state.order_manager.get_ready_orders()]  # Get a list of order IDs that are ready


    def get_order_from_customer(self, customer_id):
        o = Order(customer_id)
        self.restaurant_state.order_manager.add_order(o)  # Add the order to the restaurant state
        self.restaurant_state.assign_order_to_employee(self.employee_name, o.id)  # Assign the order to the employee
        return o.id


    def is_at_station(self, station: StationType) -> bool:
        return self.location_manager.entity_location_tile(self.employee_name).tileType == station

    def current_location(self) -> TileType:
        return self.location_manager.entity_location_tile(self.employee_name).tileType  # Get the current location of the employee

    def customer_exists(self, customer_id):
        return customer_id in self.restaurant_state.customers  # Check if the customer exists in the restaurant state
    
    def customer_status(self, customer_id) -> CustomerStatus:
        return self.restaurant_state.grab_customer(customer_id).status 
    
    def set_customer_status(self, customer_id, status):
        self.restaurant_state.grab_customer(customer_id).status = status  # Set the status of the customer in the restaurant state
    

    def _debug_current_position_of(self, entity_id: str) -> Position:
        return self.location_manager._get_entity_position(entity_id)  # Get the current position of the employee

    
    def find_station(self, stationType: StationType) -> str:
        """Finds a free station for the employee, otherwise move toward an arbitrary station"""
        current_station = self.station_manager.lookup_station_by_entity(self.employee_name)  # Check if the employee is already at a station
        if current_station is None:
            current_station = closest_station(self.employee_name, self.station_manager, self.location_manager, stationType)
        return current_station

    def lock_station(self, station_id: str, entity_id: str) -> None:
        """Locks the station for the employee"""
        station = self.station_manager.lookup_station_by_entity(entity_id)
        if station is None:
            self.station_manager.add_entity_to_station(station_id, entity_id)  # Mark the employee as at the station

    def unlock_station(self, station_id: str, entity_id: str) -> None:
        """Unlocks the station for the employee"""
        self.station_manager.remove_entity_from_station(station_id, entity_id)

    def entity_reached_entity(self, entity_id, entity2_id) -> bool:
        return self.location_manager.entity_at_entity(entity_id, entity2_id)  # Check if the employee has reached the target entity


    def approach_entity(self, approaching_entity_id: str, target_entity_id: str) -> bool:
        """Moves an entity toward another"""
        self.location_manager.move_entity_toward(approaching_entity_id, target_entity_id)
        return self.entity_reached_entity(approaching_entity_id, target_entity_id)

