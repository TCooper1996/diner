from dataclasses import dataclass
from typing import List

from src.common.events import GameEvent
from src.common.events.game_events import GameUpdateEvent
from src.core.entities.info import EntityInfo


class PauseCommandEffect():
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
class GameUpdateCommand():
    game_update: GameUpdateEvent

@dataclass
class AppCommand:  
    command:  ViewPreviousTickCommand | ViewNextTickCommand | ResizeCommand | GameUpdateCommand

class QuitEffect():
    pass

class RestartEffect():
    pass

@dataclass
class AppEffect():
    effect: QuitEffect | RestartEffect

@dataclass
class AppCommandEffect():
    command_effect: PauseCommandEffect


AppIntent = AppEffect | AppCommand | AppCommandEffect


