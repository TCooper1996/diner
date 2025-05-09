"""
Entry point for the restaurant simulator application.
This module connects the game coordinator with the UI.

The coordinator follows the clean architecture principles by acting as 
an application service that orchestrates the game loop and UI interactions.
"""

import asyncio
import threading
from queue import Queue
from typing import Any, List

from src.actions import *
from src.application.coordinator.game_ui_coordinator import GameUICoordinator
from src.application.implementations.models.GameStateImpl import GameStateImpl
from src.application.implementations.services.NavigationServiceImpl import NavigationServiceImpl
from src.application.services.AgentService import AgentServiceImpl
from src.common.event_manager import EventManager
from src.common.events import GameEvent, GuiEvent
from src.core.models.ActiveTurn import EmployeeUpdate
from src.infrastructure.navigation.build_level import build_level
from src.tui import start as start_tui



async def start_coordinator(event_manager: EventManager[GuiEvent, GameEvent], agent_service: AgentServiceImpl, nav_service: NavigationServiceImpl, employee_ordering: List[str]):
    """
    Start the game-UI coordinator.
    
    """
    def game_state_factory() -> GameStateImpl:
        """
        Factory function to create a new game state.
        
        Returns:
            A new instance of GameStateImpl.
        """
        return GameStateImpl(
            nav_service,
            agent_service,
            EmployeeUpdate(employee_ordering[0])
        )
    
    # Create and start coordinator
    coordinator = GameUICoordinator(
        event_manager=event_manager,
        game_state_factory=game_state_factory,
        employee_ordering=employee_ordering,
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
    level_file = "src/infrastructure/navigation/assets/level_1.txt"

    agent_service = AgentServiceImpl(
        instructions,
        allowed_actions,
    )

    navigation_service = NavigationServiceImpl(build_level(level_file))

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
    asyncio.run(start_coordinator(game_event_manager, agent_service, navigation_service, list(instructions.keys())))


if __name__ == "__main__":
    main()