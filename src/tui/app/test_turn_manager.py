from src.tui.app.turn_manager import TurnManager


class TestTurnSelector:
    def test_turn_selector(self):

        # Should be focused on the first turn
        t = TurnManager(0)
        assert t.is_latest_turn_focused()
        assert t.get_current() == 0
        assert t.get_previous() is None

        t.append(1)
        assert t.get_current() == 1
        assert t.get_previous() == 0

        # If focused on the latest turn, incrementing should not change the current turn
        t.increment()
        assert t.get_current() == 1

        # test decrement
        t.decrement()
        assert t.get_current() == 0
        assert t.get_previous() is None

        # Test appending a new turn when not focused on latest
        t.append(2)
        assert t.get_current() == 0
        assert t.get_previous() is None
        assert t.num_turns == 3
        assert t.is_latest_turn_focused() is False
