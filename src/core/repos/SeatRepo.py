from typing import Protocol

from src.core.entities.seat import Seat


class SeatRepo(Protocol):
    def get_seat(self, seat_id: str) -> Seat:
        ...

    def get_all_seats(self) -> list[Seat]:
        """Get all seats in the restaurant"""
        ...