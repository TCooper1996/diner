
import pygame

from src.common.event_manager import EventManager
from src.common.events import GameEvent, GuiEvent
from src.tui import canvas
from src.tui.app.game_restart_loop import game_restart_loop
from src.tui.app.loop import loop
from src.tui.canvas.canvas_state import CanvasState
from src.tui.gui.gui_state import GuiState
from src.tui.gui.make_gui import make_gui
from src.tui.gui.widgets.rect import Rect
from src.tui.gui.widgets.turn_label import TurnLabel


def start(event_manager: EventManager[GameEvent, GuiEvent]):
    pygame.init()
    height = 600
    width = 800
    surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    manager = make_gui(width, height)

    game_restart_loop(event_manager, manager, surface)
    pygame.quit()
