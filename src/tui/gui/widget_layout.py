from dataclasses import dataclass

from src.tui.gui.widgets.rect import Rect


@dataclass
class WindowLayout:
    pause_rect: Rect
    turn_rect: Rect
    canvas_rect: Rect
    message_rect: Rect


pause_height = 50
turn_height = 50
canvas_height = 400
message_rect_height = 200

def compute_layout(width: int, height: int) -> WindowLayout:
    turn_rect = Rect.new_static(0, 0, width, turn_height)
    pause_rect = Rect.new_static(0, 30, width, pause_height)

    height_left = height - pause_rect.height - turn_rect.height
    canvas_rect = Rect.new_static(0, pause_rect.bottom, width, height_left//2)
    message_rect = Rect.new_static(0, canvas_rect.bottom, width, height_left//2)
    return WindowLayout(turn_rect=turn_rect, pause_rect=pause_rect, message_rect=message_rect, canvas_rect=canvas_rect)