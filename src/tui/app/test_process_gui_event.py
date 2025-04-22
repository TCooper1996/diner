from typing import List, Optional
from src.common.events.game_events import GameUpdateEvent
from src.common.events.gui_events import *
from src.common.position import Position
from src.core.entities.info import EntityInfo
from src.core.entities.info.employee_info import EmployeeInfo
from src.tui.app.intent import *
from src.tui.app.process_gui_event import process_gui_event
from src.tui.app.window_state import GameSnapshot, WindowState


entities: List[EntityInfo] = [
    EmployeeInfo(instruction='', name="Entity2", position=Position(1, 1), turns=[]),
]
generic_update_event = AppCommand(GameUpdateCommand(GameUpdateEvent(entities, name_of_turn_entity="Entity2", turn_number=0)))

def update_event(entities: Optional[List[EntityInfo]] = None, name_of_turn_entity: str = "Entity2", turn_number: int = 0) -> AppCommand:
    if entities is None:
        entities = [
            EmployeeInfo(instruction='', name="Entity2", position=Position(1, 1), turns=[]),
        ]
    return AppCommand(GameUpdateCommand(GameUpdateEvent(entities, name_of_turn_entity=name_of_turn_entity, turn_number=turn_number)))

class TestProcessGuiEvent:
    def test_rewind(self):
        s = WindowState.default()
        # Add game updates


        # Should only update window
        e1 = update_event(name_of_turn_entity="Entity1")
        pe = process_gui_event(e1, s)
        assert pe.should_update_window == True
        assert pe.should_quit == False
        assert pe.event_to_emit is None
        s = pe.window_state
        assert s.current_turn_num == 0
        assert s.number_of_turns == 1
        assert s.focused_snapshot == GameSnapshot(entities=entities, turn_num=0, current_entity="Entity1")

        # Add another update and then test rewind
        e2 = update_event(turn_number=1, name_of_turn_entity="Entity2")
        pe = process_gui_event(e2, s)
        s = pe.window_state
        assert s.current_turn_num == 1
        assert s.number_of_turns == 2
        assert s.focused_snapshot == GameSnapshot(entities=entities, turn_num=1, current_entity="Entity2")

        pe = process_gui_event(AppCommand(ViewPreviousTickCommand()), s)
        s = pe.window_state
        assert s.current_turn_num == 0
        assert s.number_of_turns == 2
        assert s.focused_snapshot == GameSnapshot(entities=entities, turn_num=0, current_entity="Entity1")

        # Rewind again; since we're already at the first turn, it should stay the same
        pe = process_gui_event(AppCommand(ViewPreviousTickCommand()), s)
        s = pe.window_state
        assert s.current_turn_num == 0
        assert s.number_of_turns == 2
        assert s.current_entity == "Entity1"

        # Test forward
        pe = process_gui_event(AppCommand(ViewNextTickCommand()), s)
        s = pe.window_state
        assert s.current_turn_num == 1
        assert s.current_entity == "Entity2"

        # Forward again; since we're already at the last turn, it should stay the same
        pe = process_gui_event(AppCommand(ViewNextTickCommand()), s)
        s = pe.window_state
        assert s.current_turn_num == 1
        assert s.current_entity == "Entity2"

    def test_effects(self):
        s = WindowState.default()

        # Quit effect
        pe = process_gui_event(AppEffect(QuitEffect()), s)
        assert pe.should_quit == True
        assert pe.should_update_window == False
        assert pe.event_to_emit is None

        # Restart effect
        pe = process_gui_event(AppEffect(RestartEffect()), s)
        assert pe.should_quit == False
        assert pe.should_update_window == False
        assert isinstance(pe.event_to_emit, ResetGame)

        # Pause effect
        pe = process_gui_event(AppCommandEffect(PauseCommandEffect()), s)
        assert isinstance(pe.event_to_emit, Pause)
        assert pe.should_update_window == True
        assert pe.window_state == s.pause()

