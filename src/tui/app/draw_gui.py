from dataclasses import dataclass
from typing import Dict

import pygame
import pygame_gui

from src.tui.gui.widgets.rect import Rect
from pygame_gui.core import UIElement

from src.utils.benchmark import benchmark, print_time_since


@dataclass
class DrawGuiInput:
    widgets: dict[str, UIElement]
    widget_contents: dict[str, str]
    widget_rects: dict[str, Rect]


@dataclass
class WidgetState:
    text: str
    x: int
    y: int
    width: int
    height: int

delta_cache: Dict[str, WidgetState] = {}

@benchmark
def draw_gui(input_data: DrawGuiInput, update_func):
    print_time_since("draw_gui")
    widget_ids = list(input_data.widgets.keys())
    for widget_id in widget_ids:
        widget = input_data.widgets[widget_id]
        content = input_data.widget_contents[widget_id]
        rect = input_data.widget_rects[widget_id].rect

        current_state = WidgetState(
            text=content,
            x=rect.x,
            y=rect.y,
            width=rect.width,
            height=rect.height
        )

        old_state = delta_cache.get(widget_id, None)
        # If the widget is not in the cache, or if the state has changed, update it
        print_time_since("draw_gui : before cache ")
        if old_state is None or old_state != current_state:
            delta_cache[widget_id] = current_state

            widget.set_relative_position((rect.x, rect.y))

            widget.set_dimensions((rect.width, rect.height))
            
            match widget:
                case pygame_gui.elements.UILabel():
                    widget.set_text(content)
                    widget.rebuild()
                case pygame_gui.elements.UITextBox():
                    print_time_since("draw_gui : before rebuild ")
                    widget.set_text(content)
                    print_time_since("draw_gui : after set")
                    widget.rebuild()
                    print_time_since("draw_gui : after rebuild ")
        
        print_time_since("draw_gui : after cache ")
    update_func()

    print_time_since("draw_gui : after update func ")

