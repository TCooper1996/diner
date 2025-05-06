from src.core.entities.customer import Customer
from src.core.repos.CustomerRepo import CustomerRepo


class CustomerRepoImpl(CustomerRepo):
    """
    Implementation of the CustomerRepo protocol that stores customers in a dictionary.
    """

    def __init__(self):
        self._customers: dict[str, Customer] = {}

    def get_all_customers(self) -> list[Customer]:
        """
        Get all customers.
        
        Returns:
            A list of all customers.
        """
        return list(self._customers.values())

    def get_customer(self, customer_id: str) -> Customer:
        """
        Get a customer by ID.
        
        Args:
            customer_id: The ID of the customer to get.
            
        Returns:
            The customer with the specified ID.
            
        Raises:
            KeyError: If no customer exists with the specified ID.
        """
        if customer_id not in self._customers:
            raise KeyError(f"No customer found with ID {customer_id}")
        
        return self._customers[customer_id]

    def get_count(self) -> int:
        """
        Get the count of customers.
        
        Returns:
            The number of customers.
        """
        return len(self._customers)

    def add_customer(self, customer: Customer) -> None:
        """
        Add a new customer.
        
        Args:
            customer: The customer to add.
            
        Raises:
            ValueError: If a customer with the same ID already exists.
        """
        if customer.id in self._customers:
            raise ValueError(f"Customer with ID {customer.id} already exists")
        
        self._customers[customer.id] = customer

    def update_customer(self, customer: Customer) -> None:
        """
        Update an existing customer.
        
        Args:
            customer: The customer to update.
            
        Raises:
            KeyError: If no customer exists with the specified ID.
        """
        if customer.id not in self._customers:
            raise KeyError(f"No customer found with ID {customer.id} to update")
        
        self._customers[customer.id] = customer