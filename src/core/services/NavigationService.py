from typing import Protocol, TypeVar

from src.common.position import Position

class NavigationService(Protocol):
    def get_path_between_positions(self, start: Position, end: Position) -> list[Position]:
        """Get the path between two positions. includes the start and end positions"""
        ...

    def move_toward(self, start: Position, end: Position) -> Position:
        """Get the next position in the path between two positions. includes the start and end positions"""
        ...

    def get_closest_entity(self, has_position: Position, entities: list[Position]) -> int:
        """Returns the index of the closest entity in the list"""
        ...