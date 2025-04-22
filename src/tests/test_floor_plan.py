from typing import List, Literal
from src.common.position import Position
from src.infrastructure.navigation.floor_plan import FloorPlan
from src.infrastructure.navigation.tiles import Tile

TileType = Literal["_", "e", "k", "d"]
class TestFloorPlan:
    def setup_method(self):
        """Set up test environment before each test"""
        # Create a fresh game state for each test
        self.tile_types: List[TileType] = ["_", "k", "d", "e"]  # Example tile types: empty, kitchen, dining, entrance

    def test_parsing(self):
        floor_plan = """
        _ _ _ _ _
        _ K D E _ _ _ _
        """
        plan = FloorPlan[TileType](floor_plan.split('\n'), {t:t for t in self.tile_types})
        tiles = plan.tiles
        assert len(tiles[0]) == 5
        assert len(tiles[1]) == 8
        assert plan.lookup_tile((1, 1)) == Tile(tileType = "k", pos=(1, 1))
        assert plan.lookup_tile((2, 1)) == Tile(tileType = "d", pos=(2, 1))
        assert plan.lookup_tile((3, 1)) == Tile(tileType = "e", pos=(3, 1))

    def test_movement(self):
        floor_plan = """
        _ _ _ _ _
        _ K D E _ _ _ _
        """
        plan = FloorPlan(floor_plan.split('\n'), self.tile_types)
        path = plan.find_path(Position(0, 0), [Position(2, 1)])
        assert len(path) == 3, "Path should be 3 steps"
        assert path[0] == Position(0, 0)
        assert path[2] == Position(2, 1)