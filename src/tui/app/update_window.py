from dataclasses import dataclass, replace
from pathlib import Path
from typing import Dict, List
import pygame
from src.common.events.game_events import TurnSummary
from src.common.position import FPosition, Position
from src.core.entities.info import EntityInfo
from src.tui.app.draw_gui import DrawGuiInput, draw_gui
from src.tui.app.window_state import WindowState
from src.tui.canvas.canvas_state import CanvasState, create_canvas_state
from src.tui.canvas import update_canvas as _update_canvas
from src.tui.draw_level.draw_level import LevelEntityWithImage
from src.tui.gui.gui_state import GuiState
from src.tui.gui.ui_manager import UIManager
from src.tui.gui.get_gui_content import GuiDrawingContent, WidgetRects, get_gui_content
from src.tui.gui.widget_layout import WindowLayout, compute_layout
from src.tui.gui.widgets.rect import Rect
from src.tui.gui.widgets.stack.stack import stack

asset_path = Path("/Users/taylercooper/Dev/openmoji-svg-color")

"""
High level drawing function
"""

@dataclass
class UpdateWindowInput:
    entities: list[EntityInfo]
    paused: bool
    current_turn_num: int
    max_turn_num: int
    messages: List[TurnSummary]
    width: int
    height: int
    current_entity: str

    @classmethod
    def default(cls, **kwargs) -> 'UpdateWindowInput':
        d = cls(
            entities=[],
            paused=False,
            current_turn_num=0,
            max_turn_num=0,
            messages=[],
            width=800,
            height=600,
            current_entity=""
        )
        return replace(d, **kwargs)
    
    @classmethod
    def from_window_state(cls, state: WindowState) -> 'UpdateWindowInput':
        return cls(
            entities=state.focused_snapshot.entities,
            paused=state.paused,
            current_turn_num=state.current_turn_num,
            max_turn_num=state.number_of_turns,
            messages=state.focused_snapshot.turn_summaries,
            width=state.width,
            height=state.height,
            current_entity=state.focused_snapshot.current_entity
        )




def update_window(widgets: UIManager, surface: pygame.Surface, state: UpdateWindowInput, time_delta: float, entity_animation_scalar: float):
    width, height = surface.get_size()
    widgets.ui_manager.set_window_resolution((width, height))
    surface.fill((0, 0, 0))

    layout = compute_layout(state.width, state.height)

    update_canvas(layout, surface, state, entity_animation_scalar)
    update_gui(state, layout, widgets, lambda: widgets.update(time_delta, surface))
    pygame.display.flip()



def update_gui(state: UpdateWindowInput, layout: WindowLayout, widget_manager: UIManager, update_gui_func):

    g_state = GuiState(state.paused, state.current_turn_num, state.max_turn_num, state.current_entity, state.messages)
    gui_content = get_gui_content(g_state)

    widgets = {
        "turn_label": widget_manager.turn_label,
        "pause_label": widget_manager.pause_label,
        "message_box": widget_manager.message_box,
    }
    widget_contents = {
        "turn_label": gui_content.turn_label.text,
        "pause_label": gui_content.pause_label.text,
        "message_box": "\n".join(gui_content.message_box.lines,)
    }
    widget_rects = {
        "turn_label": layout.turn_rect,
        "pause_label": layout.pause_rect,
        "message_box": layout.message_rect,
    }
    input = DrawGuiInput(widgets, widget_contents, widget_rects)
    draw_gui(input, update_gui_func)


last_position_cache: Dict[str, List[Position]] = {}
def update_canvas(layout: WindowLayout, surface: pygame.Surface, state: UpdateWindowInput, entity_animation_scalar: float):


    canvas_rect = layout.canvas_rect.rect
    canvas_surface = surface.subsurface(canvas_rect)
    canvas_state = create_canvas_state(state.entities, asset_path, canvas_rect.width, canvas_rect.height)

    #Animate movement using interpolation and comparing to last unique position
    def animate_entity_position(name, position):
        if name is None:
            return position

        if name not in last_position_cache:
            last_position_cache[name] = [position]

        if last_position_cache[name][-1] != position:
            last_position_cache[name].append(position)

        if len(last_position_cache[name]) >= 2:
            start = last_position_cache[name][-2]
            end = last_position_cache[name][-1]
            # Interpolate position
            dx = (end.x - start.x) * entity_animation_scalar
            dy = (end.y - start.y) * entity_animation_scalar
            return FPosition(x=start.x + dx, y=start.y + dy)
        return position
        
    entities = [LevelEntityWithImage(animate_entity_position(e.name, e.position), e.image, e.name, e.e_type) for e in canvas_state.entities]
    new_canvas_state = replace(canvas_state, entities=entities)

    _update_canvas(new_canvas_state, canvas_surface)
