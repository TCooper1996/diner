from src.core.entities.customer import Customer
from src.core.entities.order import Order
from src.core.repos.CustomerOrderRepo import CustomerOrderRepo


class CustomerOrderRepoImpl(CustomerOrderRepo):
    """
    Implementation of the CustomerOrderRepo protocol that stores the relationships
    between customers and orders in dictionaries.
    """

    def __init__(self):
        self._customer_orders: dict[str, str] = {}  # customer_id -> order_id
        self._order_customers: dict[str, str] = {}  # order_id -> customer_id
        self._orders: dict[str, Order] = {}  # Cache for order objects
        self._customers: dict[str, Customer] = {}  # Cache for customer objects

    def associate_customer_order(self, customer: Customer, order: Order) -> None:
        """
        Associate a customer with an order.
        
        Args:
            customer: The customer to associate.
            order: The order to associate.
        """
        self._customer_orders[customer.id] = order.id
        self._order_customers[order.id] = customer.id
        
        # Cache the objects for faster retrieval
        self._orders[order.id] = order
        self._customers[customer.id] = customer

    def get_order_of_customer(self, customer_id: str) -> Order:
        """
        Get the order of a customer by their ID.
        
        Args:
            customer_id: The ID of the customer.
            
        Returns:
            The order of the customer.
            
        Raises:
            KeyError: If the customer has no associated order.
        """
        order_id = self._customer_orders.get(customer_id)
        if not order_id or order_id not in self._orders:
            raise KeyError(f"No order found for customer with ID {customer_id}")
        
        return self._orders[order_id]

    def get_customer_of_order(self, order_id: str) -> Customer:
        """
        Get the customer associated with a specific order ID.
        
        Args:
            order_id: The ID of the order.
            
        Returns:
            The customer associated with the order.
            
        Raises:
            KeyError: If the order is not associated with any customer.
        """
        customer_id = self._order_customers.get(order_id)
        if not customer_id or customer_id not in self._customers:
            raise KeyError(f"No customer found for order with ID {order_id}")
        
        return self._customers[customer_id]