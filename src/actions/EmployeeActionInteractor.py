from typing import Protocol

from src.common.position import Position
from src.core.types import StationType, TileType
from src.infrastructure.navigation.tiles import Tile
from src.core.entities.customer import CustomerStatus
from src.core.entities.order import OrderStatus



class EmployeeActionInteractor(Protocol):
    @property
    def employee_name(self) -> str:
        ...

    def get_station_locked_by(self, station_type: StationType, entity_id: str) -> str | None:
        ...

    def find_nearest_station(self, station_type: StationType, entity_id: str) -> str:
        ...


    def submit_orders(self) -> int:
        """
        Submits all unsubmitted orders that a server has taken
        Returns the number of orders submitted
        """
        ...

    def add_order_to_inventory(self, order_id: str) -> None:
        ...

    def remove_order_from_inventory(self, order_id: str) -> None:
        """
        Removes an order from the employee's inventory. This is used when an order is delivered or completed.
        """
        ...

    def order_exists(self, order_id: str) -> bool:
        ...

    def get_order_status(self, order_id: str) -> OrderStatus:
        ...


    def cook_order(self, order_id: str) -> bool:
        """Returns true if order is finished"""
        ...

    def set_order_status(self, order_id: str, status: OrderStatus) -> None:
        """
        Sets the status of an order. This is used internally to update the order's status.
        """
        ...

    def get_orders_carried(self) -> list[str]:
        """
        Returns a list of order ids that the employee is currently
        """
        ...

    def get_orders_taken(self) -> list[str]:
        """
        Returns a list of order ids that the employee has taken from customers.
        This includes orders that are in the process of being prepared or delivered.
        """
        ...

    def get_ready_orders(self) -> list[str]:
        ...


    def is_at_station(self, station: StationType) -> bool:
        """
        Checks if the employee is currently at the entrance of the restaurant.
        """
        ...

    def current_location(self) -> TileType:
        ...

    def customer_exists(self, customer_id: str) -> bool:
        ...

    def customer_status(self, customer_id: str) -> CustomerStatus:
        ...

    def set_customer_status(self, customer_id: str, status: CustomerStatus) -> None:
        ...


    def find_station(self, station: StationType) -> str:
        """Finds a station by its type and returns its id. Prioritises free stations"""
        ...


    def lock_station(self, station_id: str, entity_id) -> None:
        """Locks the station for the employee"""
        ...

    def unlock_station(self, station_id: str, entity_id) -> None:
        """Unlocks the station for the employee"""
        ...

    def _debug_current_position_of(self, entity_id: str) -> Position:
        """Use for debugging only, try not to expose the position to the business layer"""
        ...

    def entity_reached_entity(self, entity_id: str, entity2_id: str) -> bool:
        """Returns the id of the entity at the given entity"""
        ...

    def get_order_from_customer(self, customer_id: str) -> str:
        """
        Simulates taking an order from a customer. Returns the list of items ordered.
        This is used in the take order action.
        """
        ...


    def approach_entity(self, approaching_entity_id: str, target_entity_id: str) -> bool:
        """Moves an entity toward another"""
        ...
