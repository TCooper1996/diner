
from typing import Optional
from src.tui.app.intent import AppCommand, AppIntent
from src.tui.event_handling.handle_game_event import handle_game_event
from src.tui.event_handling.handle_pygame_event import handle_pygame_event
from src.tui.event_handling.types import *
from src.tui.app.window_state import WindowState
from src.tui.gui.ui_manager import UIManager


def handle_app_event(event: AppEvent, widgets: UIManager) -> Optional[AppIntent]:
    match event:
        case AppPygameEvent(e):
            intent = handle_pygame_event(e)
            widgets.process_events(e)
            return intent
        case AppGameEvent(e):
            return handle_game_event(e)
        case None:
            pass