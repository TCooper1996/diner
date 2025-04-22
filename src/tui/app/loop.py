
from pathlib import Path
from typing import List
import pygame
from dataclasses import replace
from src.common.event_manager import EventManager
from src.common.events import GameEvent, GuiEvent
from src.common.events.gui_events import ResetGame, Pause
from src.core.entities.info.employee_info import EmployeeInfo
from src.tui.app.intent import *
from src.tui.app.get_event import all_events
from src.tui.app.process_gui_event import process_gui_event
from src.tui.app.update_window import UpdateWindowInput, update_window
from src.tui.gui.ui_manager import UIManager
from src.tui.app.window_state import GameSnapshot, WindowState



def loop(state: WindowState, event_manager: EventManager[GameEvent, GuiEvent], widgets: UIManager, surface: pygame.Surface):
    clock = pygame.Clock()
    current_state = state
    running = True
    time_since_last_update = 0.0
    while running:
        time_delta = clock.tick(60)/1000
        time_since_last_update += time_delta
        for event in  all_events(event_manager, widgets):
            message = process_gui_event(event, current_state)
            if message.window_state:
                current_state = message.window_state
                # Command Effects perform side effects and update window state
            if message.event_to_emit:
                event_manager.put_event(message.event_to_emit)
            if message.should_quit:
                running = False
            if message.reset_animations:
                time_since_last_update = 0.0

        snap = UpdateWindowInput.from_window_state(current_state)
        update_window(widgets, surface, snap, time_delta, min(time_since_last_update, 1))

def handle_event_v2(event: GameEvent, state: WindowState, event_manager: EventManager[GameEvent, GuiEvent], widgets: UIManager, surface: pygame.Surface):
    """
    Handle a single event in the game loop.
    """
    message = process_gui_event(event, state)
    if message.window_state:
        state = message.window_state
    if message.event_to_emit:
        event_manager.put_event(message.event_to_emit)
    if message.should_quit:
        return False
    if message.reset_animations:
        state = replace(state, initial_snapshot=GameSnapshot.default())
    return True





