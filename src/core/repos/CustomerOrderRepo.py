from typing import Protocol

from src.core.entities.customer import Customer
from src.core.entities.order import Order


class CustomerOrderRepo(Protocol):
    def get_order_of_customer(self, customer_id: str) -> Order:
        """Get the order of a customer by their ID."""
        ...

    def get_customer_of_order(self, order_id: str) -> Customer:
        """Get the customer associated with a specific order ID."""
        ...