"""
Event handler for processing game and UI events.
"""

from dataclasses import dataclass
from typing import Callable, Dict, Protocol, TypeVar

from src.common.events import GameEvent, GuiEvent
from src.common.events.gui_events import Pause, ResetGame, ChangeTurn
from src.core.models.GameState import GameState


# Define handler protocols
class EventHandler(Protocol):
    """Protocol for event handlers."""
    def handle(self, event: object) -> None:
        """Handle an event."""
        ...


class GameEventHandler(EventHandler):
    """Handler for game events."""
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        
    def handle(self, event: GameEvent) -> None:
        """Handle a game event."""
        # Implement specific game event handling
        pass


@dataclass
class GuiEventHandler:
    """Handler for UI events."""
    pause_handler: Callable[[], None]
    reset_handler: Callable[[], None]
    change_turn_handler: Callable[[str], None]
    
    def handle(self, event: GuiEvent) -> None:
        """Handle a UI event."""
        match event:
            case Pause():
                self.pause_handler()
            case ResetGame():
                self.reset_handler()
            case ChangeTurn(turn):
                self.change_turn_handler(event.turn)
            case _:
                raise ValueError(f"Unknown GUI event type: {type(event)}")


class EventDispatcher:
    """Dispatches events to appropriate handlers."""
    def __init__(self):
        self.handlers: Dict[type, EventHandler] = {}
        
    def register_handler(self, event_type: type, handler: EventHandler) -> None:
        """Register a handler for an event type."""
        self.handlers[event_type] = handler
        
    def dispatch(self, event: object) -> None:
        """Dispatch an event to its handler."""
        event_type = type(event)
        if event_type in self.handlers:
            self.handlers[event_type].handle(event)
        else:
            # Try handling with parent class handlers
            for handler_type, handler in self.handlers.items():
                if isinstance(event, handler_type):
                    handler.handle(event)
                    return
            
            raise ValueError(f"No handler registered for event type {event_type}")