
from src.common.location import ENTRANCE
from src.core.types import TileType
from .entities import Customer
from .restaurant_state import RestaurantState


def add_customer(state: RestaurantState, customer: str | Customer, location: TileType = ENTRANCE):
    """Add a new customer to the restaurant"""
    if isinstance(customer, str):
        customer = Customer(customer)
    state.customers[customer.id] = customer
    state.location_manager.add_entity(customer.id, location)