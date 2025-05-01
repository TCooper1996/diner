
import pygame
from src.common.event_manager import EventManager
from src.common.events import GameEvent, GuiEvent
from src.tui.event_handling.handle_event import handle_app_event
from src.tui.event_handling.types import AppEvent, AppGameEvent, AppPygameEvent
from src.tui.app.window_state import WindowState
from src.tui.gui.ui_manager import UIManager


def get_event(event_manager: EventManager[GameEvent, GuiEvent] | None) -> AppEvent | None:
    event = pygame.event.poll()
    if event.type != pygame.NOEVENT:
        return AppPygameEvent(event)

    if event_manager:
        game_event = event_manager.get_event()
        if game_event is not None:
            return AppGameEvent(event=game_event)
    return None

def all_events(event_manager: EventManager[GameEvent, GuiEvent] | None, widgets: UIManager):
    while True:
        event = get_event(event_manager)
        if event is None:
            break
        else:
            command = handle_app_event(event, widgets)
            if command is not None:
                yield command