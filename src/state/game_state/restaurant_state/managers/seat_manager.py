
from dataclasses import dataclass, field
from typing import Dict



@dataclass
class Seat:
    occupant: str | None = field(default=None)

class SeatManager:
    def __init__(self, seats: Dict[str, Seat] | None = None):
        self.seats: Dict[str, Seat] = seats if seats else {}

    def __copy__(self):
        return SeatManager(self.seats.copy())

    def add_seat(self, seat_id: str):
        self.seats[seat_id] = Seat()

    def remove_seat(self, seat_id):
        if seat_id in self.seats:
            del self.seats[seat_id]

    def seat_available(self, seat_id) -> bool:
        if seat_id not in self.seats:
            return False
        return self.seats[seat_id].occupant is None

    def find_and_lock_free_seat(self, owner_id: str) -> str | None:
        for seat_id, seat in self.seats.items():
            if seat.occupant is None:
                seat.occupant = owner_id

                return seat_id
        return None

    def lookup_seat_by_owner(self, owner_id: str) -> str | None:
        """Returns the seat owned by owner_id if there is one"""
        for seat_id, seat in self.seats.items():
            if seat.occupant == owner_id:
                return seat_id
        return None 

    def get_seat(self, seat_id):
        return self.seats.get(seat_id, None)

    def list_seats(self):
        return list(self.seats.items())