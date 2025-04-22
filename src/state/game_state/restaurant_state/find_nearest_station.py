from src.core.types import StationType
from .managers import StationManager, LocationManager

def closest_station(src_entity_id: str, station_manager: StationManager, location_manager: LocationManager, station_type: StationType) -> str:
    """Finds the closest free station of the specified type"""
    stations = [s for s in station_manager.get_stations() if s.station_type == station_type]
    free_stations = [s for s in stations if s.free]

    stations_to_search = free_stations if len(free_stations) > 0 else stations
    station_ids = [station.station_id for station in stations_to_search]
    closest = location_manager.get_closest_entity(src_entity_id, station_ids)  # Find the closest station to the source entity
    return closest