from src.core.entities.customer import Customer
from src.core.entities.order import Order
from src.core.repos.CustomerOrderRepo import CustomerOrderRepo


class CustomerOrderRepoImpl(CustomerOrderRepo):
    """
    Implementation of the CustomerOrderRepo protocol that stores the relationships
    between customers and orders using a single dictionary.
    """

    def __init__(self):
        self._customer_orders: dict[str, str] = {}  # customer_id -> order_id

    def associate_customer_order(self, customer_id: str, order_id: str) -> None:
        """
        Associate a customer with an order.
        
        Args:
            customer_id: ID of the customer to associate.
            order_id: ID of the order to associate.
        """
        # Check if order is already associated with another customer
        existing_customer = self.get_customer_of_order(order_id)
        if existing_customer and existing_customer != customer_id:
            raise ValueError(f"Order {order_id} is already associated with customer {existing_customer}")
            
        self._customer_orders[customer_id] = order_id

    def get_order_of_customer(self, customer_id: str) -> str:
        """
        Get the order ID of a customer by their ID.
        
        Args:
            customer_id: The ID of the customer.
            
        Returns:
            The order ID of the customer.
            
        Raises:
            KeyError: If the customer has no associated order.
        """
        order_id = self._customer_orders.get(customer_id)
        if not order_id:
            raise KeyError(f"No order found for customer with ID {customer_id}")
        
        return order_id

    def get_customer_of_order(self, order_id: str) -> str:
        """
        Get the customer ID associated with a specific order ID.
        
        Args:
            order_id: The ID of the order.
            
        Returns:
            The customer ID associated with the order, or None if not found.
        """
        order_customers = {v: k for k, v in self._customer_orders.items()}
        return order_customers[order_id]