
from pathlib import Path
from typing import Literal
from src.common.events import GameEvent
from src.common.events.game_events import GameUpdateEvent
from src.core.entities.info import *
from src.tui import canvas
from src.tui.app.intent import AppCommand, GameUpdateCommand
from src.tui.draw_level.draw_level import LevelEntityWithImage
from src.tui.emojis import get_emoji
from src.tui.app.window_state import WindowState
from src.tui.emojis.emojis import station_emojis

asset_dir = Path("/Users/taylercooper/Dev/openmoji-svg-color")

def handle_game_event(event: GameEvent) -> AppCommand:
    match event:
        case GameUpdateEvent():
            return AppCommand(GameUpdateCommand(event))
        case _:
            raise NotImplementedError(f"Unhandled game event type: {type(event).__name__}")
