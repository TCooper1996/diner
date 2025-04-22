
from dataclasses import dataclass

from src.common.position import Position
from src.core.types import StationType


@dataclass
class StationInfo:
    station_id: str
    position: Position
    station_type: StationType

    @property
    def name(self) -> str:
        return self.station_id