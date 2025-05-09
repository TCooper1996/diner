from typing import Protocol



class CustomerOrderRepo(Protocol):
    def get_order_of_customer(self, customer_id: str) -> str:
        """Get the order of a customer by their ID."""
        ...

    def get_customer_of_order(self, order_id: str) -> str:
        """Get the customer associated with a specific order ID."""
        ...