
from pathlib import Path
from typing import Literal
from src.common.events import GameEvent
from src.common.events.game_events import GameUpdateEvent
from src.core.entities.info import *
from src.tui import canvas
from src.tui.app.intent import AppCommand, GameUpdateCommand

def handle_game_event(event: GameEvent) -> AppCommand:
    match event:
        case GameUpdateEvent():
            return GameUpdateCommand(event)
        case _:
            raise NotImplementedError(f"Unhandled game event type: {type(event).__name__}")
