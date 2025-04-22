
from dataclasses import dataclass

import pygame

from src.common.event_manager import EventManager
from src.common.events import GameEvent, GuiEvent


@dataclass
class AppGameEvent:
    event: GameEvent

@dataclass
class AppPygameEvent:
    event: pygame.event.Event

AppEvent = AppGameEvent | AppPygameEvent

WindowEventManager = EventManager[GameEvent, GuiEvent]