from typing import Protocol
from src.core.entities.customer import Customer
from src.core.entities.seat import Seat
from src.core.repos import SeatRepo
from src.core.services import NavigationService


class CustomerSeatService(Protocol):
    def find_closest_seat_to_customer(self, customer: str) -> Seat:
        """
        Get the customer seat information for a given customer ID.
        """
        # Placeholder for actual implementation
        pass