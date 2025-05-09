from dataclasses import dataclass, replace
from pathlib import Path
from typing import Dict, List
import pygame
from src.common.position import FPosition, Position
from src.tui.app.draw_gui import DrawGuiInput, draw_gui
from src.tui.app.window_state import WindowState
from src.tui.canvas import update_canvas as _update_canvas
from src.tui.gui.gui_state import GuiState, GuiTurnSummary
from src.tui.gui.ui_manager import UIManager
from src.tui.gui.get_gui_content import  get_gui_content
from src.tui.gui.widget_layout import WindowLayout, compute_layout
asset_path = Path("/Users/taylercooper/Dev/openmoji-svg-color")

"""
High level drawing function
"""

def update_window(widgets: UIManager, surface: pygame.Surface, state: WindowState, time_delta: float):
    width, height = surface.get_size()
    widgets.ui_manager.set_window_resolution((width, height))
    surface.fill((0, 0, 0))

    layout = compute_layout(get_canvas_aspect_ratio(state), state.width, state.height)

    update_canvas(layout, surface, state)
    update_gui(state, layout, widgets, lambda: widgets.update(time_delta, surface))
    pygame.display.flip()


def get_canvas_aspect_ratio(state: WindowState) -> float:
    floors = state.game_snapshot.get_navigation_service().get_floor_plan()
    width = max(f.x for f in floors) + 1
    height = max(f.y for f in floors) + 1
    return width / height

def update_gui(state: WindowState, layout: WindowLayout, widget_manager: UIManager, update_gui_func):
    gui_turn_summary = GuiTurnSummary(state.game_snapshot.get_whose_turn(), state.game_snapshot.get_turn_summary())
    g_state = GuiState(state.paused, state.current_turn_num, state.max_turn, state.game_snapshot.whose_turn(), gui_turn_summaries )
    gui_content = get_gui_content(g_state)

    widgets = {
        "turn_label": widget_manager.turn_label,
        "pause_label": widget_manager.pause_label,
        "message_box": widget_manager.message_box,
    }
    widget_contents = {
        "turn_label": gui_content.turn_label.text,
        "pause_label": gui_content.pause_label.text,
        "message_box": "\n".join(reversed(gui_content.message_box.lines))
    }
    widget_rects = {
        "turn_label": layout.turn_rect,
        "pause_label": layout.pause_rect,
        "message_box": layout.message_rect,
    }
    input = DrawGuiInput(widgets, widget_contents, widget_rects)
    
    draw_gui(input, update_gui_func)


last_position_cache: Dict[str, List[Position]] = {}
def update_canvas(layout: WindowLayout, surface: pygame.Surface, state: WindowState):
    canvas_rect = layout.canvas_rect.rect
    canvas_surface = surface.subsurface(canvas_rect)
    entity_repo = state.game_snapshot.entity_repo

    # Prepare dictionaries for employees, customers, and stations
    positions = {e.name: e.position for e in entity_repo.employees}
    positions.update({c.name: c.position for c in entity_repo.customers})
    positions.update({f"{s.position.x},{s.position.y}": s.position for s in entity_repo.stations})


    customer_names = [c.name for c in entity_repo.customers]
    employee_names = [e.name for e in entity_repo.employees]
    station_ids = [f"{s.position.x},{s.position.y}" for s in entity_repo.stations]
    station_types = {f"{s.position.x},{s.position.y}": s.station_type for s in entity_repo.stations}
    floor_plan = [f.position for f in entity_repo.floors]


    _update_canvas(canvas_surface, positions,  customer_names, employee_names, station_ids, station_types, floor_plan)
