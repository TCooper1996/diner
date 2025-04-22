import copy
from typing import Dict, Literal, TypeVar
from src.common.position import Position
from src.infrastructure.navigation.floor_plan import FloorPlan
from src.state.managers.location_manager import LocationManager

T = TypeVar("T")
TileType = Literal["_", "e", "k", "d", "m"]  

class TestLocationManagerWrapper[T](LocationManager[T]):
    def __init__(self, floor_plan: FloorPlan[T], entity_locations: Dict[str, Position] | None = None):
        super().__init__(floor_plan, entity_locations)

    def __copy__(self):
        return TestLocationManagerWrapper(self.floor_plan, self._entity_locations.copy())

    def __getitem__(self, entity_id: str) -> Position:
        return self._get_entity_position(entity_id)

class TestLocationManager:
    def setup_method(self):
        floor_data = """
        _ _ _ _ _
        _ K D E _ _ _ M
        """
        floor_plan = FloorPlan[TileType](floor_data.split('\n'), {k:k for k in ["_", "k", "d", "e", "m"]})  # Example tile types: empty, kitchen, dining, entrance
        key_map = {
            "k": "kitchen",
            "d": "dining",
            "e": "entrance"
        }
        self.location_manager = TestLocationManagerWrapper(floor_plan, key_map)

    def test_add_entity(self):
        # Adds an entity to a random kitchen tile, which should be (1,1) in this case
        self.location_manager.add_entity("employee1", "k")
        assert self.location_manager._get_entity_position("employee1") == Position(1, 1), "Employee should be at kitchen tile (1, 1)"


    def test_move_entity_toward(self):
        self.location_manager.add_entity("employee1", "k")
        self.location_manager.add_entity("employee2", "m")
        assert self.location_manager["employee1"] == Position(1, 1), "Employee1 should start at kitchen tile (1, 1)"

        new_man = lambda: copy.copy(self.location_manager)  # Copy the location manager to avoid side effects

        prepared = new_man()
        prepared.move_entity_toward("employee1", "employee2", steps=1)
        assert prepared["employee1"] == Position(2, 1), "Employee1 should move to dining tile (2, 1) after 1 step"
        # After moving 1 step, employee1 should be at the dining tile (2, 1)

        prepared2 = new_man()
        prepared2.move_entity_toward("employee1", "employee2", steps=3)
        assert prepared2["employee1"] == Position(4, 1), "Employee1 should move to dining tile (4, 1) after 1 step"

