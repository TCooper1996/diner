
from dataclasses import dataclass

from src.common.events import *
from src.tui.app.intent import *
from src.tui.app.window_state import WindowState
from .process_window_command import process_window_command


@dataclass
class ProcessedGuiEvent:
    window_state: WindowState | None = None
    event_to_emit: GuiEvent | None = None
    should_quit: bool = False
    reset_animations: bool = False

    @property
    def should_update_window(self) -> bool:
        return self.window_state is not None


def process_gui_event(event: AppIntent, current_state: WindowState) -> ProcessedGuiEvent:
    match event:
        # Commands simply update the window state, no side effects
        case AppCommand(command):
            new_state = process_window_command(current_state, event)
            return ProcessedGuiEvent(window_state=new_state, reset_animations=isinstance(command, (GameUpdateCommand, ViewPreviousTickCommand, ViewNextTickCommand)))
        # Effects may communicate with the game loop but do not update window state
        case AppEffect(effect):
            match effect:
                case QuitEffect():
                    return ProcessedGuiEvent(should_quit=True)
                    
                case RestartEffect():
                    return ProcessedGuiEvent(event_to_emit=ResetGame(), window_state=current_state.restart())

        case AppCommandEffect(command_effect):
            match command_effect:
                case PauseCommandEffect():
                    current_state = current_state.pause()
                    return ProcessedGuiEvent(window_state=current_state, event_to_emit=Pause())

        case unknown_event:
            raise NotImplementedError(f"Event {unknown_event} not implemented")