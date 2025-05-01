
from dataclasses import dataclass, field
from email import message
from typing import Dict, List
from src.actions import Action
from src.actions.wait import WaitAction
from src.agents.models.Model import StandardMessage
from src.core.entities.customer import Customer
from src.core.types import StationType, TileType
from src.game_engine.active_turn import ActiveTurn, EmployeeUpdate
from src.game_engine.config import Config, create_config
from src.game_engine.select_employee_action import SelectActionUsecase
from src.game_engine.verify_employee_action import verify_employee_action
from src.infrastructure.navigation.floor_plan import FloorPlan
from src.state.employee import employee
from src.state.employee.employee import Employee
from src.state.game_state.restaurant_state.add_customer import add_customer
from src.state.game_state.restaurant_state.add_employee import add_employee
from src.state.game_state.restaurant_state.initialize_entities import initialize_entities
from src.state.game_state.restaurant_state.managers.location_manager import LocationManager
from src.state.game_state.restaurant_state.managers.order_manager import OrderManager
from src.state.game_state.restaurant_state.managers.station_manager import StationManager
from src.state.game_state.restaurant_state.restaurant_state import EntityType, RestaurantState



@dataclass
class GameLoopState:
    restaurant_state: RestaurantState
    employees_current_actions: Dict[str, Action | None]
    active_turn: ActiveTurn
    tick: int
    config: Config
    messages: Dict[str, List[StandardMessage]]



async def game_loop(instructions: Dict[str,str], floor_plan: FloorPlan[TileType]) -> None:
    config = create_config()
    r_state =  create_restaurant_state(instructions, floor_plan)
    whose_turn = EmployeeUpdate(0)
    names = list(instructions.keys())
    state = GameLoopState(state, {n: None for n in names}, whose_turn, 0, config)
    while True:
        match whose_turn:
            case EmployeeUpdate(index=index):
                employee_update(state, names[index])
                employee_name = names[index]
                action = await get_action_from_agent(employee_name, state)
                state, next_action = run_employee_action(state, employee_name, action)
                state.employees_current_actions[employee_name] = next_action
                whose_turn = EmployeeUpdate(index=(index + 1) % len(state.employees))
            case CustomerUpdate():
                customer_turn_record = run_customer_update(state, state.tick)
                whose_turn = EmployeeUpdate(0)
            case _:
                raise Exception("Invalid substate")


async def employee_update(loopstate: GameLoopState, state: RestaurantState, employee_name: str) -> None:
    # Choose action
    choose_next_action


@dataclass
class Attempt:
    selected_action: Action
    text_response: StandardMessage
    tool_invocation: StandardMessage
    validation_error: str | None = None
async def repeat_until_valid_action(employee_name: str, loopstate: GameLoopState, state: RestaurantState, messages: List[StandardMessage]) -> Action:

    responses = []
    for i in range(3):
        messages = loopstate.messages[employee_name]
        response = await loopstate.config.agent_service.invoke_agent(employee_name, state.to_prompt(), messages)
        result = verify_employee_action(response.selected_action, state, employee_name)
        
        responses.append(Attempt(response.selected_action, response.text_response, response.tool_invocation,  result.error_msg))
        # If the action is valid, return it
        if result.success:
            return responses, response
        # Check to see if the action is valid
    raise Exception(f"Failed to get a valid action for {employee_name} after 3 attempts. Last attempt: {responses[-1].validation_error}")

def create_restaurant_state(instructions: Dict[str, str], level: FloorPlan[TileType]) -> RestaurantState:
    employees = {n: Employee(name=n, instruction=i, current_action=WaitAction()) for n, i in instructions.items()}
    location_manager = LocationManager[TileType](level)
    customer = Customer()
    restaurant_state = RestaurantState(
        location_manager=location_manager,
    )
    add_customer(restaurant_state, customer, "entrance")  # Ensure the first customer is added
    for e in employees.values():
        add_employee(restaurant_state, e.name, e.instruction, "entrance")

    initialize_entities(restaurant_state)
    return restaurant_state