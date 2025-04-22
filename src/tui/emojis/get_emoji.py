
from pathlib import Path
from typing import Dict

from pygame import Surface

from src.tui.emojis.get_unused_face import get_unused_face
from src.core.entities.info import *
from src.tui.emojis.get_emoji_image import get_emoji_image
from .emojis import station_emojis


def get_emoji(entity: EntityInfo, asset_dir: Path) -> Surface:
    emoji = select_emoji(entity)
    return get_emoji_image(asset_dir, emoji)

def select_emoji(entity: EntityInfo) -> str:
    match entity:
        case EmployeeInfo(name=name):
            return get_unused_face(name)
        case CustomerInfo(name=name):
            return get_unused_face(name)
        case StationInfo(station_type=station_type):
            return station_emojis[station_type]
        case FloorInfo():
            return station_emojis["floor"]
        case _:
            raise ValueError(f"Unknown entity type: {entity}")