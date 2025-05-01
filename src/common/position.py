
from dataclasses import dataclass

@dataclass
class FPosition:
    x: float
    y: float

    @classmethod
    def from_position(cls, position: 'Position') -> 'FPosition':
        return cls(float(position.x), float(position.y))


@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return self.x == other[0] and self.y == other[1]

    def __str__(self):
        return f"(x={self.x}, y={self.y})"