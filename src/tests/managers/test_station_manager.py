

from src.state.game_state.restaurant_state.managers.station_manager import StationManager


class TestStationManager:
    def setup_method(self):
        self.man = StationManager()

    def test_locking(self):
        self.man.add_station("kitchen1", "kitchen")
        free_station = self.man.find_free_station("kitchen")  # Should return None as no cooking station is available
        assert free_station == "kitchen1"

        # Assert that adding an employee locks it
        self.man.add_entity_to_station("kitchen1", "employee1")
        free_station2 = self.man.find_free_station("kitchen")
        assert free_station2 == None

        # Assert that removing the employee frees the station
        self.man.remove_entity_from_station("kitchen1", "employee1")
        free_station3 = self.man.find_free_station("kitchen")
        assert free_station3 == "kitchen1"
