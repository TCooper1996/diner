from dataclasses import dataclass
from typing import List
from src.tui.gui.gui_state import GuiState
from src.tui.gui.ui_manager import UIManager
from src.tui.gui.widgets import *
from src.tui.gui.widgets.rect import Rect
from src.tui.gui.widgets.stack.stack import stack

@dataclass
class WidgetRects:
    turn_label: Rect
    pause_label: Rect
    message_box: Rect

@dataclass
class GuiDrawingContent:
    turn_label: TurnLabel
    pause_label: PauseLabel
    message_box: MessageBox


def get_gui_content(state: GuiState):

    turn_label = build_turn_label(state)
    pause_label = build_pause_label(state)
    message_box = build_message_box(state)
    return GuiDrawingContent(
        turn_label=turn_label,
        pause_label=pause_label,
        message_box=message_box)


def build_turn_label(state: GuiState) -> TurnLabel:
    return TurnLabel(f"{state.current_turn_num}/{state.max_turn_num} - Entity: {state.current_entity}")

def build_pause_label(state: GuiState) -> PauseLabel:
    return PauseLabel("Paused" if state.paused else "Running")

def build_message_box(state: GuiState) -> MessageBox:
    messages = []
    if state.messages:
        block = []
        block.append(f"<b>Turn: {turn_summary['entity_name']}</b>")
        block.append(f"<strong>Action</strong>: {turn_summary['action']}")
        if turn_summary['agent_response']:
            block.append(f"<strong>Agent Response</strong>: {turn_summary['agent_response'].rstrip()}")
        block.append(f"<strong>Result</strong>: {turn_summary['action_result']}")
        messages.append("\n".join(block) + "\n")
    return MessageBox(messages)
