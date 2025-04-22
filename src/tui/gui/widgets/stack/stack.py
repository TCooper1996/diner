from typing import Dict, List
from pygame_gui.core import UIElement


def stack(widgets: List[int], spacing: int = 0) -> List[int]:
    out_widgets: List[int] = []
    start_y = 0
    y = start_y
    for w in widgets:
        out_widgets.append(y)
        y += (spacing + w)
    return out_widgets

