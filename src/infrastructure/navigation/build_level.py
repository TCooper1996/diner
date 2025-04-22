from typing import Dict
from src.core.types import TileType
from src.infrastructure.navigation.floor_plan import FloorPlan


def build_level(level_asset_path: str) -> FloorPlan:
    level_lines = open(level_asset_path, 'r').readlines()
    floor_keys: Dict[str, TileType] = {
        "_": "floor",
        "k": "kitchen",
        "d": "dining",
        "e": "entrance"
    }
    return FloorPlan(level_lines, floor_keys)