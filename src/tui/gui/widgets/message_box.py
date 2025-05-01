from dataclasses import dataclass
from typing import List, TypedDict

from pygame import Rect


@dataclass
class MessageBox:
    lines: List[str]