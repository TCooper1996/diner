"""
Coordinator that manages the interaction between the game loop and UI.
This follows the clean architecture principle of keeping application logic separate
from UI and infrastructure concerns.
"""

import asyncio
import os
from queue import Queue
from typing import Optional, List, Dict, Any, Callable, Coroutine

from src.application.implementations.models.GameStateImpl import GameStateImpl
from src.common.event_manager import EventManager
from src.common.events import GameEvent, GuiEvent
from src.common.events.game_events import GameUpdateEvent, NewGameEvent
from src.common.events.gui_events import ResetGame, Pause, ChangeTurn
from src.common.pause_manager import PauseManager
from src.core.models.GameState import GameState
from src.application.loop.game_loop import game_loop
from src.infrastructure.navigation.build_level import build_level


class GameUICoordinator:
    """
    Coordinates between the game loop and UI, based on clean architecture principles.
    
    Responsibilities:
    - Translates UI events into game commands
    - Processes game state updates and sends them to the UI
    - Handles game lifecycle events (pause, restart, quit)
    - Manages the game loop execution and coordination with UI
    
    This replaces the older GameController implementation with a more modular design
    that better separates concerns between the game loop, UI, and coordination logic.
    """
    
    def __init__(self, 
                 event_manager: EventManager[GuiEvent, GameEvent],
                 game_state_factory: Callable[[], GameState],
                 employee_ordering: List[str]):
        """
        Initialize the coordinator with dependencies.
        
        Args:
            agent_service: Service to interact with AI agents
            event_manager: Manager for passing events between game and UI
        """
        self.event_manager = event_manager
        self.pause_manager = PauseManager()
        self.current_game_task: Optional[asyncio.Task] = None
        self.reset_event = asyncio.Event()
        self.game_state_factory = game_state_factory
        self.employee_ordering = employee_ordering
    
    @property
    def paused(self) -> bool:
        """Check if the game is currently paused."""
        return self.pause_manager.is_paused()
    
    async def start(self):
        """
        Start the coordinator, listening for UI events and managing the game loop.
        
        This is the main entry point that starts:
        1. The event handling loop
        2. The initial game loop
        3. Manages restarting the game when requested
        """
        # Start event handling loop
        event_handler_task = asyncio.create_task(self.handle_events())
        
        # Create a loop that restarts the game when needed
        while True:
            # Clear the reset event
            self.reset_event.clear()
            
            # Initialize a new game
            initial_state = self.game_state_factory()
            
            # Notify the UI a new game is starting
            initial_update = GameUpdateEvent(initial_state)
            self.event_manager.put_event(NewGameEvent(initial_update))
            
            # Start game loop
            game_loop_task = asyncio.create_task(
                self.run_game_loop(initial_state, self.employee_ordering)
            )
            self.current_game_task = game_loop_task
            
            # Wait for a reset event
            await self.reset_event.wait()
            
            # Cancel existing game
            if not game_loop_task.done():
                game_loop_task.cancel()
                try:
                    await game_loop_task
                except asyncio.CancelledError:
                    print("Game loop cancelled for restart")
            
            # Small delay before restarting
            await asyncio.sleep(0.1)
    
    async def run_game_loop(self, initial_state: GameStateImpl, employee_ordering: List[str]):
        """
        Run the game loop with the given initial state and employee ordering.
        
        This processes each game state update from the generator and sends updates to the UI.
        """
        try:
            game_generator = game_loop(initial_state, employee_ordering)
            
            # Process each state update from the generator
            async for current_state in game_generator:
                # Skip updates if paused
                if not self.paused:
                    # Convert the game state to a UI update event
                    update_event = GameUpdateEvent(current_state)
                    # Send to UI
                    self.event_manager.put_event(update_event)
                
                # Respect pause state - allow UI to catch up
                while self.pause_manager.is_paused():
                    await asyncio.sleep(0.1)
                
                # Small delay between turns for better UI experience
                await asyncio.sleep(0.1)
        
        except asyncio.CancelledError:
            # Clean cancellation (e.g., when restarting game)
            raise
        
        except Exception as e:
            # Log other exceptions but don't crash
            print(f"Error in game loop: {e}")
    
    
    async def handle_events(self):
        """
        Process events from the UI, translating them to game commands.
        
        This handles events like:
        - Pause/resume
        - Game reset
        - Turn navigation (for UI playback)
        """
        while True:
            # Non-blocking check for UI events
            await asyncio.sleep(0.1)
            event = self.event_manager.get_event()
            
            if event is None:
                continue
            
            # Handle different event types
            if isinstance(event, Pause):
                self.pause_manager.toggle()
                print(f"Game {'paused' if self.paused else 'resumed'}")
            
            elif isinstance(event, ResetGame):
                print("Resetting game...")
                if os.path.exists("responses.json"):
                    os.remove("responses.json")
                # Signal to restart the game
                self.reset_event.set()
            
            
            else:
                print(f"Unhandled event type: {type(event)}")