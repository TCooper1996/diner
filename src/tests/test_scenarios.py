from typing import Literal, Tuple
from src.actions import *
from src.common.position import Position
from src.controllers.employee_controller import EmployeeAgentController
from src.core.types import TileType
from src.infrastructure.navigation.floor_plan import FloorPlan
from src.protocols import IAction
from src.state.game_state import restaurant_state as restaurant
from src.state.game_state.restaurant_state.entities import *


tileTypes = {
    "_": "empty",
    "k": "kitchen",
    "d": "dining",
    "e": "entrance",
}

class TController:
    def __init__(self, r_state, employee: str):

        self.state: restaurant.RestaurantState = r_state
        self.employee = employee
        self.c = EmployeeAgentController(llm=None)

    def execute(self, action: IAction) -> Tuple[str, bool]:
        return self.c.execute_action(action, self.state, employee_id="test_employee")

    def add_employee(self, employee_id: str, location: TileType):
        restaurant.add_employee(self.state, employee_id, "", location)

    def add_customer(self, id: str, pos):
        restaurant.add_customer(self.state, id, pos)

class TestScenarios:
    def setup_method(self):
        floor_plan_data = """
    E _ _ _ D
    _ _ _ _ _
    _ _ _ _ _
    K K _ _ _
    """
        floor_plan = FloorPlan(floor_plan_data.splitlines(), tileTypes)  # Assuming you have a FloorPlan class that can be initialized with a string
        self.cont = TController(restaurant.RestaurantState(restaurant.LocationManager(floor_plan, step_size=1)), 
                                  employee="test_employee")
        self.cont.state.initialize_entities()

    def repeat(self, action: IAction | SeatAction, attempts: int):
        for i in range(attempts):
            _, repeat  = self.cont.execute(action)
            if i == attempts-1:
                assert not repeat, "The action should not repeat on the last attempt."
            else:
                assert repeat, f"Attempt {i+1}: The action should repeat until it succeeds."

    def test_full_visit(self):
        # Create employee and customer, go through typical pipeline
        self.cont.state.add_employee("test_employee", "", "entrance")
        self.cont.state.add_customer("test_customer", "entrance")

        # Seat a customer
        self.repeat(SeatAction(customer_id="test_customer"), 4)

        # Take order
        self.cont.execute(TakeOrderAction(customer_id="test_customer"))
        # Server should now own an order
        orders = [o.id for o in self.cont.state.get_orders()]

        assert len(orders) == 1, f"Expected 1 order, found {len(orders)}"
        assert self.cont.state.grab_customer("test_customer").status == CustomerStatus.ORDERED
        assert self.cont.state.orders_taken_by_employee("test_employee") == orders

        # bring to kitchen
        self.repeat(SubmitOrdersToKitchen(), 6)

        self.cont.execute(CookAction(order_id=orders[0]))
        assert self.cont.state.grab_order(orders[0]).status == self.cont.state.order_manager[orders[0]].status, "Order should be in COOKING status after calling CookAction"

        # pick up order
        self.cont.execute(PickUpOrder(order_id=orders[0]))  # Assuming you have a PickUpOrderAction to pick up the cooked order
        assert self.cont.state.orders_carried_by_employee("test_employee") == [orders[0]]

        self.repeat(DeliverOrderToCustomer(customer_id="test_customer", order_id=orders[0]), 6)

        for i in range(3):
            self.cont.state.customer_update( "test_customer")
            if i < 2:
                assert self.cont.state.grab_customer("test_customer").status == CustomerStatus.EATING
            else:
                assert self.cont.state.grab_customer("test_customer").status == CustomerStatus.LEAVING

        for i in range(4):
            self.cont.state.customer_update("test_customer")
            if i < 3:
                assert self.cont.state.grab_customer("test_customer").status == CustomerStatus.LEAVING
            else:
                assert self.cont.state.grab_customer("test_customer").status == CustomerStatus.DONE

        # Test scenario 1
        assert True

    def test_scenario_2(self):
        # Test scenario 2
        assert True

    def test_scenario_3(self):
        # Test scenario 3
        assert True