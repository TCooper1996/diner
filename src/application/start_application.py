"""
Entry point for the restaurant simulator application.
This module connects the game coordinator with the UI.

The coordinator follows the clean architecture principles by acting as 
an application service that orchestrates the game loop and UI interactions.
"""

import asyncio
import threading
from queue import Queue
from typing import Any

from src.actions import *
from src.application.coordinator.game_ui_coordinator import GameUICoordinator
from src.application.services.AgentService import AgentService
from src.common.event_manager import EventManager
from src.common.events import GameEvent, GuiEvent
from src.tui import start as start_tui


async def start_coordinator(event_manager: EventManager[GuiEvent, GameEvent], agent_service: AgentService):
    """
    Start the game-UI coordinator.
    
    """
    
    # Create and start coordinator
    coordinator = GameUICoordinator(
        agent_service=agent_service,
        event_manager=event_manager
    )
    
    # Start and await coordinator
    await coordinator.start()


def main():
    """
    Main entry point for the application.
    
    This function:
    1. Creates the event manager for communication between game and UI
    2. Starts the UI in a separate thread
    3. Starts the game coordinator in the main thread
    """

    instructions = {
        "Alice": "You will seat customers as they come in.", 
        "Bob": "After Alice seats customers, you will take their orders and bring the orders to the kitchen to be submitted. "
                "Once the orders are ready, bring them to their respective customers.", 
        "Jim": "As Bob brings you orders, you must cook them. "
                "If there are no orders to cook, then wait."}
    allowed_actions: Dict[str, Any] = {
        "Alice": [WaitAction, SeatAction],
        "Bob": [WaitAction, TakeOrderAction, SubmitOrdersToKitchen, PickUpOrder, DeliverOrderToCustomer],
        "Jim": [WaitAction, CookAction]
    }

    agent_service = AgentService(
        instructions,
        allowed_actions,
    )
    # Create queues for bi-directional communication
    game_to_ui_queue = Queue()
    ui_to_game_queue = Queue()
    
    # Create event managers for both directions
    ui_event_manager = EventManager(in_q=game_to_ui_queue, out_q=ui_to_game_queue)
    game_event_manager = EventManager(in_q=ui_to_game_queue, out_q=game_to_ui_queue)
    
    # Start UI in separate thread
    ui_thread = threading.Thread(
        target=lambda: start_tui(ui_event_manager), 
        daemon=True
    )
    ui_thread.start()
    
    # Start game coordinator in main thread
    asyncio.run(start_coordinator(game_event_manager, agent_service))


if __name__ == "__main__":
    main()