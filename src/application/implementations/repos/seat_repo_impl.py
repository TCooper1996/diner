from src.core.entities.seat import Seat
from src.core.repos.SeatRepo import SeatRepo


class SeatRepoImpl(SeatRepo):
    """
    Implementation of the SeatRepo protocol that stores seats in a dictionary.
    """

    def __init__(self):
        self._seats: dict[str, Seat] = {}

    def get_seat(self, seat_id: str) -> Seat:
        """
        Get a seat by ID.
        
        Args:
            seat_id: The ID of the seat to get.
            
        Returns:
            The seat with the specified ID.
            
        Raises:
            KeyError: If no seat exists with the specified ID.
        """
        if seat_id not in self._seats:
            raise KeyError(f"No seat found with ID {seat_id}")
        
        return self._seats[seat_id]

    def get_all_seats(self) -> list[Seat]:
        """
        Get all seats in the restaurant.
        
        Returns:
            A list of all seats.
        """
        return list(self._seats.values())
    
    def add_seat(self, seat: Seat) -> None:
        """
        Add a seat to the repository.
        
        Args:
            seat: The seat to add.
            
        Raises:
            ValueError: If a seat with the same ID already exists.
        """
        if seat.seat_id in self._seats:
            raise ValueError(f"Seat with ID {seat.seat_id} already exists")
        
        self._seats[seat.seat_id] = seat