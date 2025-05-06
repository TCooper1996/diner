from src.core.entities.seat import Seat
from src.core.repos.CustomerSeatRepo import CustomerSeatRepo


class CustomerSeatRepoImpl(CustomerSeatRepo):
    """
    Implementation of the CustomerSeatRepo protocol that manages the relationship
    between customers and seats using dictionaries.
    """

    def __init__(self):
        self._customer_seats: dict[str, str] = {}  # customer_name -> seat_id
        self._seat_customers: dict[str, str] = {}  # seat_id -> customer_name
        self._seats: dict[str, Seat] = {}  # seat_id -> Seat (cache)

    def add_seat(self, seat: Seat) -> None:
        """
        Add a seat to the repository.
        
        Args:
            seat: The seat to add.
        """
        self._seats[seat.id] = seat

    def get_customer_seat(self, customer_name: str) -> Seat | None:
        """
        Get the seat of a customer.
        
        Args:
            customer_name: The name of the customer.
            
        Returns:
            The seat of the customer, or None if the customer is not seated.
        """
        seat_id = self._customer_seats.get(customer_name)
        if not seat_id:
            return None
        
        return self._seats.get(seat_id)

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
        if seat_id in self._seat_customers and self._seat_customers[seat_id] != customer_name:
            raise ValueError(f"Seat {seat_id} is already occupied by {self._seat_customers[seat_id]}")
        
        # If the customer already has a seat, remove that association
        if customer_name in self._customer_seats:
            old_seat_id = self._customer_seats[customer_name]
            if old_seat_id in self._seat_customers:
                del self._seat_customers[old_seat_id]
        
        # Set the new association
        self._customer_seats[customer_name] = seat_id
        self._seat_customers[seat_id] = customer_name

    def is_occupied(self, seat_id: str) -> bool:
        """
        Check if a seat is occupied.
        
        Args:
            seat_id: The ID of the seat to check.
            
        Returns:
            True if the seat is occupied, False otherwise.
        """
        return seat_id in self._seat_customers