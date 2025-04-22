
import copy
from typing import List, Protocol, Tuple
from src.actions import Action, parse_tool
from src.agents.employeeAgent import LLM, LLMResult
from src.agents.models.Model import Model, ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.controllers.employeeActionInteractorAdapter import EmployeeActionInteractorAdapter
from src.state.game_state.immutable_types import EmployeeDecision
from langchain_core.messages import HumanMessage
from src.state.game_state.game_state import GameState
from src.state.game_state.immutable_types.employee_turn import EmployeeTurn
from src.state.game_state.restaurant_state.restaurant_state import RestaurantState
from src.state.game_state.restaurant_state.entities import Employee


class EmployeeAgentController:
    def __init__(self, llm: LLM):
        self.llm = llm

    async def process(self, gameState: GameState, employeeId: str) -> EmployeeTurn:
        employee = gameState.restaurant_state.grab_employee(employeeId)

        action = employee.current_action
        action_to_execute = None
        decisions = []
        if action is None:
            decisions = await self.choose_next_valid_action(gameState, employee)
            action_to_execute = decisions[-1].get_action()
        else:
            action_to_execute = action

        message, repeat = self.execute_action(action_to_execute, gameState.restaurant_state, employeeId)
        new_state = gameState.restaurant_state#copy.copy(gameState.restaurant_state)  # Create a copy of the restaurant state to return
        next_action = action_to_execute if repeat else None
        employee.current_action = next_action  # Update the employee's current action to the next action if not repeating
        return EmployeeTurn(employee_name=employeeId, decisions=decisions, action_result_message=message, next_action = next_action, action=action_to_execute, new_state = new_state)

    def execute_action(self, action: Action, restaurant_state: RestaurantState, employee_id: str) -> Tuple[str, bool]:
        adapter = EmployeeActionInteractorAdapter()
        interactor = adapter.from_restaurant_state(restaurant_state, employee_id)
        seat_result = action.execute(interactor)
        return seat_result.message, seat_result.repeat

        
    async def choose_next_valid_action(self, gameState: GameState, employee: Employee) -> List[EmployeeDecision]:
        decisions: List[EmployeeDecision] = []
        messages = gameState.employee_messages(employee.name)
        print(employee.name)
        for i in range(3):
            decision = await self.choose_next_action(gameState.restaurant_state, employee.name, employee.instruction, [*messages, *gather_messages(decisions)])
            decisions.append(decision)
            print("\t" + decision.get_response())
            if decision.was_valid:
                return decisions
            print("\t FAILED")


        raise Exception(f"Failed to process action for employee {employee} after 3 attempts")
        


    async def choose_next_action(self, r_state: RestaurantState, name: str, instruction: str, messages: List[StandardMessage]) -> EmployeeDecision:

        state_message_content = f"Your name is : {name}. \nCurrent game state:\n{r_state.to_prompt()}"
        state_message = HumanMessage(content=state_message_content)
        
        response =  await self.llm.invoke_cached(name, instruction, state_message, messages)
        action = parse_tool(response.tool_name, response.tool_args)
        interactor = EmployeeActionInteractorAdapter().from_restaurant_state(r_state, name)
        validation_result = action.is_valid(interactor)
        tool_output = "Tool invocation successful" if validation_result.success else f"Tool invocation failed: {validation_result.error_msg}"
        return EmployeeDecision(action=action, 
                                 response=ResponseMessage(content=response.original_response.content),
                                 result=ToolResultMessage(tool=response.tool_name, tool_id= response.tool_id, tool_output=tool_output, is_error=not validation_result.success),
                                 invocation=ToolInvocationMessage(tool=response.tool_name, tool_input=response.tool_args, tool_id=response.tool_id),
                                 state_message=state_message_content,
                                 messages=[repr(m) for m in messages] if messages else [],
                                 )


def gather_messages(decisions: List[EmployeeDecision]) -> List[StandardMessage]:
    new_messages = []
    for d in decisions:
        new_messages.extend(d.get_messages())
    return new_messages