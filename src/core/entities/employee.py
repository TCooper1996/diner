from dataclasses import dataclass

from src.common.position import Position


@dataclass
class Employee:
    name: str
    instructions: str
    position: Position