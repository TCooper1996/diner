from collections import deque
from dataclasses import dataclass
from typing import ClassVar, Dict, List, Literal, Tuple, TypeVar

from src.common.position import Position
from src.infrastructure.navigation.LevelViewTile import LevelViewTile
from src.infrastructure.navigation.tiles import Tile, T


class FloorPlan[T]:
    def __init__(self, raw_data: List[str], tile_types: Dict[str, T]):
        self.raw_data = raw_data
        self.tile_types: Dict[str, T] = {t.lower():v for t,v in tile_types.items()}
        trimmed: List[str] = []
        for line in raw_data:
            new_line = "".join([t for t in line.lower() if t in self.tile_types])
            if len(new_line) > 0:
                trimmed.append(new_line)

        final = []
        for y, line in enumerate(trimmed):
            _new_line: List[Tile[T]] = []
            for x, char in enumerate(line):
                pos = Position(x=x, y=y)
                tile = Tile(pos=pos, tileType=self.tile_types[char])
                _new_line.append(tile)
            final.append(_new_line)
        self.tiles:List[List[Tile]] = final

    def get_neighbors(self, tile: Position) -> List[Position]:
        neighbors = []
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            x = tile.x + dx
            y = tile.y + dy
            if x < 0 or y < 0:
                continue
            if y >= len(self.tiles) or x >= len(self.tiles[y]):
                continue
            neighbors.append(Position(x=x, y=y))
        return neighbors

    def lookup_tile(self, pos: Position | Tuple[int, int]) -> Tile:
        if isinstance(pos, tuple):
            pos = Position(x=pos[0], y=pos[1])
        return self.tiles[pos.y][pos.x]
    
    def find_tile_of_type(self, room: str) -> Tile:
        for row in self.tiles:
            for tile in row:
                if tile.tileType == room:
                    return tile
        raise ValueError(f"No tile of type {room} found")

    def find_path(self, current_tile: Position, destinations: List[Position]) -> List[Position]:
        """Find the shortest path from current_tile to any of the destinations."""
        if self.lookup_tile(current_tile).pos in destinations:
            return [current_tile]

        r = find_shortest_path(current_tile, lambda pos: pos in destinations, self.get_neighbors)
        if r is None:
            raise ValueError("No path found")

        return r

    def get_tiles(self) -> List[Tile]:
        tiles = []
        for row in self.tiles:
            tiles.extend(row)
        return tiles
        

    def print_level(self, entities: List[Position]):
        occupant_dict = {}
        for pos in entities:
            # Count the number of entities at each position
            if pos not in occupant_dict:
                occupant_dict[pos] = 1
            occupant_dict[pos] += 1

        grid = self.tiles
        views = self.mapGrid(grid, lambda tile: LevelViewTile(location=tile.room, occupants = occupant_dict.get(tile.pos, 0)))
        strings = self.mapGrid(views, lambda tile: tile.to_string())
        return "\n".join(["".join(line) for line in strings])


    def mapGrid(self, grid: List[List[Tile]], func):
        return [[func(cell) for cell in row] for row in grid]
    
                


def find_shortest_path(start, is_goal, get_neighbors):
    queue = deque([(start, [])])
    visited = set([start])
    
    while queue:
        current, path = queue.popleft()
        if is_goal(current):
            return path + [current]
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [current]))
    
    return None  # no path found