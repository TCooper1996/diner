
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Literal

from pygame import Surface

from src.tui.emojis.get_unused_face import get_unused_face
from src.tui.emojis.get_emoji_image import get_emoji_image
from .emojis import station_emojis


def get_face_emoji(name:str, asset_dir: Path) -> Path:
    return get_emoji_image(asset_dir, get_unused_face(name))

def get_station_emoji(station_type: str, asset_dir: Path) -> Path:
    if station_type not in station_emojis:
        raise ValueError(f"Unknown station type: {station_type}")
    return get_emoji_image(asset_dir, station_emojis[station_type])

def get_floor_emoji(asset_dir: Path) -> Path:
    return get_emoji_image(asset_dir, station_emojis["floor"])
