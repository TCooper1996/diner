from dataclasses import dataclass

from src.common.position import Position


@dataclass
class Seat:
    seat_id: str
    position: Position