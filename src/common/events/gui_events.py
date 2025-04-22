from dataclasses import dataclass
from typing import Literal


@dataclass
class ClearHistory():
    pass

@dataclass
class Pause():
    pass

@dataclass
class ResetGame():
    pass

@dataclass
class ChangeTurn():
    turn: Literal["next", "previous"]

