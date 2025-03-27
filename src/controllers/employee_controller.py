
from typing import List, Protocol
from src.actions import parse_tool
from src.actions.wait import WaitAction
from src.agents.employeeAgent import LLM, LLMResult
from src.agents.models.Model import Model, ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.state.employee.EmployeeDecision import EmployeeDecision
from src.state.employee.EmployeeTurn import EmployeeTurn
from src.state.employee.employee import Employee
from langchain_core.messages import HumanMessage
from src.state.restaurant_state import RestaurantState

class AgentTalker(Protocol):
    async def invoke(self, prompt: str, state_message: StandardMessage) -> LLMResult:
        ...

class EmployeeAgentController:


    async def process(self, agentTalker: AgentTalker, restaurant_state: RestaurantState, employeeId: str) -> EmployeeTurn:
        employee = restaurant_state.grab_employee(employeeId)

        action = employee.current_action
        action_to_execute = None
        decisions = []
        if action == WaitAction():
            decisions = await self.choose_next_valid_action(agentTalker, restaurant_state, employee)
            action_to_execute = decisions[-1].get_action()
        else:
            action_to_execute = action

        result = action_to_execute.execute(employee, restaurant_state)
        next_action = action_to_execute if result.repeat() else WaitAction()
        return EmployeeTurn(employee_name=employeeId, decisions=decisions, action_result_message=result.result_message, next_action = next_action, action=action_to_execute, new_state = result.new_state)


        


    async def choose_next_valid_action(self, agentTalker: AgentTalker, restaurant_state: RestaurantState, employee: Employee) -> List[EmployeeDecision]:
        decisions = []
        for i in range(3):
            decision = await self.choose_next_action(agentTalker, restaurant_state, employee)
            decisions.append(decision)
            if decision.was_valid:
                return decisions


        raise Exception(f"Failed to process action for employee {employee} after 3 attempts")
        


    async def choose_next_action(self, agentTalker: AgentTalker, restaurant_state: RestaurantState, employee: Employee) -> EmployeeDecision:
        state_message = HumanMessage(content=f"Your name is : {employee.name}. \nCurrent game state:\n{restaurant_state.to_prompt()}")
        
        response =  await agentTalker.invoke(employee.instruction, state_message)
        action = parse_tool(response.tool_name, response.tool_args)
        validation_result = action.is_valid(employee, restaurant_state)
        tool_output = "Tool invocation successful" if validation_result.success else f"Tool invocation failed: {validation_result.error_msg}"
        return EmployeeDecision(action=action, 
                                 response=ResponseMessage(content=response.original_response.content),
                                 result=ToolResultMessage(tool=response.tool_name, tool_id= response.tool_id, tool_output=tool_output, is_error=not validation_result.success),
                                 invocation=ToolInvocationMessage(tool=response.tool_name, tool_input=response.tool_args, tool_id=response.tool_id),
                                 )


