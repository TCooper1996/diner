from collections import deque
from dataclasses import dataclass
from typing import ClassVar, Dict, List

from src.game_engine.location import Location
from src.infrastructure.navigation.position import Position
from src.infrastructure.navigation.tiles import Tile



TileTypes: Dict[str, Location] = {"_": "floor", "K": "kitchen", "D": "dining", "E": "entrance"}
class FloorPlan:
    def __init__(self, raw_data: List[str]):
        self.raw_data = raw_data
        trimmed: List[str] = []
        for line in raw_data:
            new_line = "".join([t for t in line if t in TileTypes])
            if len(new_line) > 0:
                trimmed.append(new_line)

        final = []
        for y, line in enumerate(trimmed):
            _new_line: List[Tile] = []
            for x, char in enumerate(line):
                pos = Position(x=x, y=y)
                tile = Tile(pos=pos, room=TileTypes[char])
                _new_line.append(tile)
            final.append(_new_line)
        self.tiles:List[List[Tile]] = final

    def get_neighbors(self, tile: Position) -> List[Position]:
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x = tile.x + dx
                y = tile.y + dy
                if x < 0 or y < 0:
                    continue
                if y >= len(self.tiles) or x >= len(self.tiles[y]):
                    continue
                neighbors.append(Position(x=x, y=y))
        return neighbors

    def lookup_tile(self, pos: Position) -> Tile:
        return self.tiles[pos.y][pos.x]

    def get_next_tile(self, current_tile: Position, destination: Location) -> Position:
        r = find_shortest_path(current_tile, lambda t: self.lookup_tile(t).room == destination, self.get_neighbors)
        if r is None:
            raise ValueError("No path found")
        return r[0]

    def get_tiles(self) -> List[Tile]:
        tiles = []
        for row in self.tiles:
            tiles.extend(row)
        return tiles
        
    
                


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