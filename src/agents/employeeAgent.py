from dataclasses import dataclass
import time
from typing import Coroutine, Dict, List, Annotated, TypedDict, Callable, Any, Optional, Tuple
import os
import json

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage, SystemMessage

from src.agents.observe import observe_environment
from src.state.employee import Employee
from src.state.game import GameState
from src.game_engine.location import Location
from src.state.types import AgentDecision, EmployeeTurn
from src.utils.env import get_anthropic_api_key

# Import actions from the new actions package
from src.actions import *

planning_template = """
You are {name}, an employee at a diner. Your instructions are: '{instruction}'

Only perform duties relevant to your instructions.


Here is additional information about the restaurant:
- Orders are created when the 'TakeOrder' tool is used in the dining area where there are customers who haven't ordered yet.
- A newly created order is in the 'pending' state.
- Orders are moved to the 'TAKEN' state when the 'NotifyKitchenOfOrders' tool is used in the kitchen.
- Orders are moved to the 'COOKING' state when the 'Cook' tool is used in the kitchen.
- Orders are moved to the 'READY' state when they are ready to be delivered to the customer.
- Orders are moved to the 'DELIVERED' state when they are delivered to the customer.
- Orders move strictly in the following order: pending -> taken -> cooking -> ready -> delivered

Based on your instructions and the current state of the restaurant,
decide what you should do next.

Here is the current state of the restaurant:
{observation}            
End of restaurant state.

Here are some of your recent thoughts and actions:
{recent_thoughts}

Plan your actions 2-3 steps ahead, describe your next move and rationale, and choose an action
"""
@dataclass
class LLMResult:
    tool_name: str
    tool_args: Dict[str, Any]
    tool_id: str
    prompt: str
    original_response: BaseMessage

class ClaudeLLM:
    """LLM for the employee agent"""
    def __init__(self):
        self.model = "chatgpt"
        # Setup the LLM
        load_dotenv()
        chatgpt="gpt-4o-mini-2024-07-18"
        claude = "claude-3-5-haiku-latest"
        self.llm = ChatAnthropic(
            model=claude,
            temperature=0,
            anthropic_api_key=get_anthropic_api_key(),
        )

    async def invoke(self, prompt, state_message, messages) -> LLMResult:
        system_message = SystemMessage(content=prompt)
        
        # Explicit query at the end
        human_message = HumanMessage(content="""
    First, provide a short (one-sentence) summary of your next planned steps.
    Then, immediately invoke exactly one available tool to carry out your very next action.
    """)

        llm = self.llm.bind_tools(create_tools())

        start = time.perf_counter()
        response = await llm.ainvoke([
            system_message,
            state_message,
            *messages,
            human_message
        ])
        end = time.perf_counter()
        
        print(f"LLM response time: {end - start} seconds")

        result = LLMResult(
            tool_name=response.tool_calls[0]["name"],
            tool_args=response.tool_calls[0]["args"],
            tool_id=response.tool_calls[0]["id"],
            original_response=response,
            prompt=prompt
        )
        return result    
    

class LlamaLLM:
    def __init__(self):
        self.llm = ChatOllama(model="mistral", temperature=0, verbose=True)

    async def invoke(self, prompt: str, messages: List[BaseMessage]) -> LLMResult:
        system_message = SystemMessage(content=prompt)
        

        # Explicit query at the end
        query_message = HumanMessage(content="Based on the instructions, game state, and recent actions, what action should I perform next?")

        llm = self.llm.bind_tools(create_tools())

        start = time.perf_counter()
        response = await llm.ainvoke([
            system_message,
            *messages,
            query_message
        ])
        end = time.perf_counter()
        
        print(f"LLM response time: {end - start} seconds")

        result = LLMResult(
            tool_name=response.tool_calls[0]["name"],
            tool_args=response.tool_calls[0]["args"],
            tool_id=response.tool_calls[0]["id"],
            original_response=response,
            prompt=prompt
        )
        return result



# Employee controller class that processes employee actions
class EmployeeAgentController:
    def __init__(self, llm: ClaudeLLM | None = None):
        self.llm = llm if llm else ClaudeLLM()

    async def process(self, gameState: GameState, employeeId: str) -> List[AgentDecision]:
        return await self.process_recursive(gameState, employeeId, 0)

    async def process_recursive(self, _gameState: GameState, employeeId: str, attempt: int) -> List[AgentDecision]:
        gameState = _gameState.model_copy(deep=True)
        employee = gameState.employees[employeeId]
        state_message = HumanMessage(content=f"Current game state:\n{gameState.to_prompt()}")
        response = await self.llm.invoke(employee.instruction, state_message, employee.messages)
        self.last_response = response
        # Update the employee's messages with the response
        action = parse_tool(response.tool_name, response.tool_args)
        # Set the employee's action directly to avoid any type issues
        # Does the response need to be saved to memory?
        employee.add_message(response.original_response)

        # This is a copy, do not try to mutate the original employee or game state
        result = performAction(gameState, employee, action)

        result.game_state.grab_employee(employeeId).add_message(ToolMessage(content=result.message, type="tool", tool_call_id=response.tool_id, status="success" if result.success else "error"))

        if result.success:
            # Update the game state with the result
            return [AgentDecision(action=action, actionResult=result)]
        elif attempt < 3:
            # Retry the action
            return [AgentDecision(action=action, actionResult=result), *await self.process_recursive(result.game_state, employeeId, attempt + 1)]
        else:
            raise Exception(f"Failed to process action for employee {employeeId} after 3 attempts")

def performAction(gameState: GameState, employee: Employee, toolResult: EmployeeAction) -> ActionResult:
    match (toolResult):
        case MoveToNewRoom():
            return validate_move_to_location(employee, gameState, toolResult)
        case SeatAction():
            return seat_customer(employee, gameState, toolResult)
        case TakeOrderAction():
            return take_order(employee, gameState, toolResult)
        case CookAction():
            return cook_food(employee, gameState, toolResult)
        case HandOrderToCustomer():
            return hand_food_to_customer(employee, gameState, toolResult)
        case WaitAction():
            return validate_wait(employee, gameState)
        case SubmitOrdersToKitchen():
            return validate_submit_orders_to_kitchen(employee, gameState)
        case _:
            raise Exception(f"Unknown tool: {toolResult}")