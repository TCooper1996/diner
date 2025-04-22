
from src.common.events.gui_events import ChangeTurn, ClearHistory, Pause, ResetGame
from src.tui.event_handling.types import WindowEventManager


def reset(event_producer: WindowEventManager):
    """Reset the window to its initial state."""
    event_producer.put_event(ResetGame())

def next_turn(event_producer: WindowEventManager):
    """Advance to the next turn in the game."""
    event_producer.put_event(ChangeTurn(turn="next"))

def previous_turn(event_producer: WindowEventManager):
    """Go back to the previous turn in the game."""
    event_producer.put_event(ChangeTurn(turn="previous"))

def clear_history(event_producer: WindowEventManager):
    event_producer.put_event(ClearHistory())

def pause(event_producer: WindowEventManager):
    event_producer.put_event(Pause())
    print("Game paused.")