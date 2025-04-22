
from dataclasses import dataclass

from src.common.location import Location


@dataclass
class LevelViewTile:
    location: Location
    occupants: int

    def to_string(self):
        if self.occupants > 0:
            return str(self.occupants)
        return self.location[0]