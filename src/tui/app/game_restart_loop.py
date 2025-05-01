import time 
import pygame
from src.common.event_manager import EventManager
from src.common.events import GameEvent, GuiEvent
from src.common.events.game_events import GameUpdateEvent, NewGameEvent
from src.common.events.gui_events import ResetGame
from src.tui.app.loop import loop
from src.tui.gui.ui_manager import UIManager


def game_restart_loop(event_manager: EventManager[GameEvent, GuiEvent], widgets: UIManager, surface: pygame.Surface):
    """
    Main loop for restarting the game.
    """
    while True:
        event = event_manager.get_event()
        if isinstance(event, NewGameEvent):
            end = loop(event.update, event_manager, widgets, surface)
            if end == "Restart":
                event_manager.put_event(ResetGame())
                continue
            elif end == "Quit":
                return
            else:
                raise ValueError(f"Unexpected loop end reason: {end}")
        elif event is not None:
            raise ValueError(f"Unexpected event type: {type(event)}. Expected only NewGameEvent.")
        time.sleep(0.1)