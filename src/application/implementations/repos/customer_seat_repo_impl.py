from src.core.entities.seat import Seat
from src.core.repos.CustomerSeatRepo import CustomerSeatRepo


class CustomerSeatRepoImpl(CustomerSeatRepo):
    """
    Implementation of the CustomerSeatRepo protocol that manages the relationship
    between customers and seats using dictionaries.
    """

    def __init__(self):
        self._customer_seats: dict[str, str] = {}  # customer_name -> seat_id


    def get_customer_seat(self, customer_name: str) -> str | None:
        return self._customer_seats.get(customer_name)

    def set_customer_seat(self, customer_name: str, seat_id: str) -> None:
        """
        Assign a seat to a customer.
        
        Args:
            customer_name: The name of the customer.
            seat_id: The ID of the seat to assign.
            
        Raises:
            ValueError: If the seat is already occupied by another customer.
        """
        # Check if the seat is already occupied by another customer
        if self.get_customer_of_seat(seat_id) and self.get_customer_of_seat(seat_id) != customer_name:
            raise ValueError(f"Seat {seat_id} is already occupied by {self.get_customer_of_seat(seat_id)}")
        
        
        # Set the new association
        self._customer_seats[customer_name] = seat_id

    def is_seat_occupied(self, seat_id: str) -> bool:
        """
        Check if a seat is occupied.
        
        Args:
            seat_id: The ID of the seat to check.
            
        Returns:
            True if the seat is occupied, False otherwise.
        """
        return self.get_customer_of_seat(seat_id) is not None

    def get_seat_of_customer(self, customer_name: str) -> str | None:
        return self._customer_seats.get(customer_name)

    def get_customer_of_seat(self, seat_id: str) -> str | None:
        seat_customers =  {v: k for k, v in self._customer_seats.items()}
        return seat_customers.get(seat_id)