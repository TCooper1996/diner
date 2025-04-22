from functools import reduce
from typing import Dict, List, Protocol, TypeVar
from src.common.location import Location
from src.common.position import Position
from src.infrastructure.navigation.tiles import Tile

T = TypeVar("T")

class IFloorPlan[T](Protocol):
    def get_tiles(self) -> List[Tile[T]]:
        ...

    def find_path(self, current_tile: Position, destinations: List[Position]) -> List[Position]:
        ...


class LocationManager[T]:
    def __init__(self, floor_plan: IFloorPlan[T], entity_locations: Dict[str, Position] | None = None, step_size: int = 5):
        self._entity_locations: Dict[str, Position] = entity_locations if entity_locations else {}
        self.floor_plan: IFloorPlan[T] = floor_plan
        self.step_size = step_size

    def __copy__(self):
        return LocationManager(self.floor_plan, self._entity_locations.copy(), self.step_size)

    def _get_entity_position(self, entity_id: str) -> Position:
        if entity_id not in self._entity_locations:
            raise ValueError(f"Entity {entity_id} not found.")
        return self._entity_locations[entity_id]

    def get_closest_entity(self, entity_id: str, destination_ids: List[str]) -> str:
        destination_poss = {id: self._get_entity_position(id) for id in destination_ids}
        src_pos = self._get_entity_position(entity_id)
        paths = []
        for id, pos in destination_poss.items():
            path = self.floor_plan.find_path(src_pos, [pos])
            paths.append((id, len(path)))

        sorted_paths = sorted(paths, key=lambda x: x[1])  # Sort by path length
        return sorted_paths[0][0]

    def get_positions_of_tile_type(self, tile_key: T) -> List[Position]:
        return [t.pos for t in self.floor_plan.get_tiles() if t.tileType == tile_key]
        


    def add_entity(self, entity_id: str, tile_key: T | Position):
        if isinstance(tile_key, Position):
            self._entity_locations[entity_id] = tile_key
        else:
            pos = self.get_random_tile_of_type(tile_key)  # Ensure the location is valid
            self._entity_locations[entity_id] = pos

    def update_entity(self, entity_id:str, new_position: Position):
        self._entity_locations[entity_id] = new_position

    def move_entity_toward(self, entity_id: str, dest_entity: str) -> bool:
        path = self.find_path(entity_id, dest_entity)

        new_pos = path[self.step_size] if len(path) > self.step_size else path[-1]
        self._entity_locations[entity_id] = new_pos
        return new_pos == path[-1]

    def steps_to_entity(self, entity_id: str, dest_entity: str) -> int:
        path = self.find_path( entity_id, dest_entity)
        return len(path)//self.step_size

    def find_path(self, entity_id: str, dest_entity: str) -> List[Position]:
        if entity_id not in self._entity_locations:
            raise ValueError(f"Entity {entity_id} not found.")
        
        if dest_entity not in self._entity_locations:
            raise ValueError(f"Destination {dest_entity} not found.")
        
        start = self._get_entity_position(entity_id)
        end = self._get_entity_position(dest_entity)
        return self.floor_plan.find_path(start, [end])

    def entity_location_tile(self, entity_id: str) -> Tile[T]:
        entity_pos = self._get_entity_position(entity_id)
        tiles = self.floor_plan.get_tiles()
        return [t for t in tiles if t.pos == entity_pos][0]

    def get_closest_tile_of_type(self, entity_id: str, tile_key: T) -> Tile[T]:
        start = self._get_entity_position(entity_id)
        closest_tile = None
        closest_tile_distance = 100000
        tiles = [t for t in self.floor_plan.get_tiles() if t.tileType == tile_key]
        for tile in tiles:
            distance = len(self.floor_plan.find_path(start, [tile.pos]))
            if distance < closest_tile_distance:
                closest_tile_distance = distance
                closest_tile = tile
        if closest_tile is None:
            raise ValueError(f"No tiles of type {tile_key} found.")
        return closest_tile



    def get_random_tile_of_type(self, key: T) -> Position:
        for tile in self.floor_plan.get_tiles():
            if tile.tileType == key:
                return tile.pos
        raise ValueError(f"No tiles of type {key} found")

    def entity_at_entity(self, entity_id: str, target_entity_id: str) -> bool:
        """Checks if two entities are at the same position"""
        if entity_id not in self._entity_locations:
            raise ValueError("Entity {entity_id} not found.")
        if target_entity_id not in self._entity_locations:
            raise ValueError("Target entity {target_entity_id} not found.")

        return self._entity_locations[entity_id] == self._entity_locations[target_entity_id]