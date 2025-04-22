
import asyncio
import copy
from dataclasses import dataclass
from itertools import chain
from queue import Empty, Queue
import threading
from typing import Dict, List, Tuple, TypeVar
from src import tui
from src.common.event_manager import EventManager
from src.common.events import *
from src.game_engine.GameController import GameController




def start_pygame(event_manager: EventManager[GameEvent, GuiEvent]):
    tui.start(event_manager)

def main():
    gameToGuiQueue = Queue()
    guiToGameQueue = Queue()
    gui_event_manager = EventManager(in_q=gameToGuiQueue, out_q=guiToGameQueue)
    game_event_manager = EventManager(in_q=guiToGameQueue, out_q= gameToGuiQueue)
    game_thread = threading.Thread(target=lambda: asyncio.run(GameController(game_event_manager).start_game_loop()), daemon=True)
    game_thread.start()

    start_pygame(gui_event_manager)

if __name__ == "__main__":
    main()

