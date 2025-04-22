from dataclasses import dataclass
from typing import Dict, List, TypeVar

T = TypeVar("T")
@dataclass
class Station[T]:
    station_type: T
    acquired: List[str] # List of employees that are at or approaching the station for use

@dataclass
class StationInfo[T]:
    station_id: str
    station_type: T
    free: bool


class StationManager[T]:
    def __init__(self, stations: Dict[str, Station[T]] | None= None):
        self.stations: Dict[str, Station[T]] = stations if stations else {}

    def add_station(self, station_id, station_type: T):
        """Add a new station to the manager."""
        if station_id in self.stations:
            raise ValueError(f"Station with ID {station_id} already exists.")
        self.stations[station_id] = Station(station_type=station_type, acquired=[])

    def find_free_station(self, station_type: T) -> str | None:
        """Find a free station of the specified type. Returns the station ID if found, otherwise None."""
        for station_id, station in self.stations.items():
            if station.station_type == station_type and len(station.acquired) == 0:
                return station_id
        return None

    def grab_station(self, station_id: str) -> StationInfo[T]:
        """Retrieve a station by its ID."""
        if station_id not in self.stations:
            raise ValueError(f"Station with ID {station_id} does not exist.")
        s = self.stations[station_id]

        return StationInfo(station_id, s.station_type, free=(len(s.acquired) == 0))

    def find_station(self, station_type: T) -> str:
        for station_id, station in self.stations.items():
            if station.station_type == station_type:
                return station_id
        raise ValueError

    def add_entity_to_station(self, station_id: str, employee_id: str):
        self.stations[station_id].acquired.append(employee_id)

    def remove_entity_from_station(self, station_id: str, employee_id: str):
        self.stations[station_id].acquired.remove(employee_id)

    def lookup_station_by_entity(self, employee_id: str) -> str | None:
        """Returns the station ID where the employee is currently located or headed, if any."""
        for station_id, station in self.stations.items():
            if employee_id in station.acquired:
                return station_id
        return None
    
    def get_stations(self) -> List[StationInfo[T]]:
        """Returns a dictionary of station IDs with their types and availability."""
        return [StationInfo(station_id=station_id, station_type=station.station_type, free=(station.acquired == 0))
                for station_id, station in self.stations.items()]
    
    def __copy__(self):
        return StationManager(self.stations.copy())
