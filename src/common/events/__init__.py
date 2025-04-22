from .game_events import *
from .gui_events import *

GuiEvent = Pause | ClearHistory | ResetGame | ChangeTurn

GameEvent = GameUpdateEvent