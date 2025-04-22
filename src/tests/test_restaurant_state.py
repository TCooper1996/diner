

from typing import Literal
from src.actions.seat import SeatAction
from src.controllers.EmployeeActionInteractor import EmployeeActionInteractor
from src.controllers.employee_controller import EmployeeAgentController
from src.infrastructure.navigation.floor_plan import FloorPlan
from src.protocols import IAction
from src.state.game_state.restaurant_state.managers.location_manager import LocationManager
from src.state.game_state.restaurant_state.restaurant_state import RestaurantState

TileType= Literal["empty", "kitchen", "dining", "entrance"]
tileTypes = {
    "_": "empty",
    "k": "kitchen",
    "d": "dining",
    "e": "entrance",
}

class TestController:
    def __init__(self, r_state):

        self.state = r_state
        self.c = EmployeeAgentController(llm=None)

    def execute(self, action: IAction | SeatAction):
        self.c.execute_action(action, self.state, employee_id="test_employee")


class TestRestaurantState:
    def setup_method(self):
        floor_plan_data = """
    E _ _ _ D
    _ _ _ _ D
    _ _ _ _ D
    K K _ _ _
    """
        floor_plan = FloorPlan(floor_plan_data.splitlines(), tileTypes)  # Assuming you have a FloorPlan class that can be initialized with a string
        self.cont = TestController(RestaurantState(LocationManager(floor_plan)))

    def test_seating(self):  
        self.cont.state.initialize_entities()
        assert len(self.cont.state.get_seats()) == 3

    def test_add_employee(self):
        self.cont.state.add_employee("test_employee", "entrance")
        self.cont.state.add_customer()
        assert len(self.cont.state.employees) == 1
        assert self.cont.state.get_employee("test_employee").location == "entrance"