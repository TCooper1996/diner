from dataclasses import dataclass
from typing import Protocol

from src.core.entities.seat import Seat


class CustomerSeatRepo(Protocol):
    def get_customer_seat(self, customer_name: str) -> str | None:
        """Get the seat number of a customer"""
        ...
    
    def set_customer_seat(self, customer_name: str, seat_id: str):
        ...

    def is_seat_occupied(self, seat_id: str) -> bool:
        """Check if a seat is occupied"""
        ...