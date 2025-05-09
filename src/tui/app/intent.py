from dataclasses import dataclass
from typing import List

from src.common.events import GameEvent
from src.common.events.game_events import GameUpdateEvent


class PauseCommand():
    pass

class ViewPreviousTickCommand():
    pass

class ViewNextTickCommand():
    pass

@dataclass
class ResizeCommand():
    width: int
    height: int

@dataclass
class QuitCommand():
    pass

@dataclass
class RestartCommand():
    pass

@dataclass
class GameUpdateCommand():
    game_update: GameUpdateEvent

AppCommand = ViewPreviousTickCommand | ViewNextTickCommand | ResizeCommand | GameUpdateCommand | QuitCommand | RestartCommand | PauseCommand


