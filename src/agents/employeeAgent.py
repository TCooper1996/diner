import asyncio
from dataclasses import dataclass
import time
from typing import Coroutine, Dict, List, Annotated, TypedDict, Callable, Any, Optional, Tuple
import os
import json
import pickle

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage, SystemMessage

from src.agents.models.Model import Model, ResponseMessage, ToolInvocationMessage, ToolResultMessage
from src.agents.observe import observe_environment
from src.state.employee import Employee, EmployeeTurn
from src.state.game import GameState
from src.game_engine.location import Location
from src.state.types import AgentDecision
from src.utils.env import get_anthropic_api_key

# Import actions from the new actions package
from src.actions import *
from src.actions.base import ActionResult

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
    original_response: ResponseMessage

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

class LLM:
    """LLM for the employee agent"""
    def __init__(self, model: Model):
        self.model = model
        # Setup the LLM
        llamaLLM = ChatOllama(
            model="mistral",
            temperature=0
        )

    async def invoke_cached(self, prompt, state_message, messages) -> LLMResult:
        # caching
        cache = {}
        if os.path.exists("responses.json"):
            with open("responses.json", "rb") as f:
                cache = pickle.load(f)
        key = str({"prompt": prompt, "state_message": state_message, "messages": [repr(m) for m in messages]})
        if key in cache:
            return cache[key]
        response = await self.invoke(prompt, state_message, messages)
        cache[key] = response
        with open("responses.json", "wb") as f:
            pickle.dump(cache, f)
        return response

    async def invoke(self, prompt, state_message, _messages) -> LLMResult:
        
        system_message = SystemMessage(content=prompt)
        messages = [*_messages]

        if len(messages) > 0:
            if messages[-1].is_error:
                messages.append(HumanMessage(content="Tool invocation failed: Your last action was invalid. Try again."))
            else:
                messages.append(HumanMessage(content="Tool invocation successful"))
        
        # Explicit query at the end
        human_message = HumanMessage(content="""
        You must invoke exactly ONE tool provided to you.
    """)

        i = -1
        while True:
            i += 1
            start = time.perf_counter()
            text, tool_call = await self.model.ainvoke([
                system_message,
                state_message,
                *messages,
                human_message
            ])
            end = time.perf_counter()

            if tool_call is None:
                if i > 3:
                    raise Exception("Failed to get a valid response from the LLM")
                messages = [*messages, text, HumanMessage(content="Error: You must invoke exactly one tool. Try again.")]
                continue
            
            print(f"LLM response time: {end - start} seconds")

            result = LLMResult(
                tool_name=tool_call.tool,
                tool_args=tool_call.tool_input,
                tool_id=tool_call.tool_id,
                original_response=text,
                prompt=prompt
            )
            return result    
    




# Employee controller class that processes employee actions
class EmployeeAgentController:
    def __init__(self, llm: Model):
        self.llm = LLM(llm)

    async def process(self, gameState: GameState, employeeId: str) -> GameState:
        return await self.process_recursive(gameState, employeeId, 0)

    async def process_recursive(self, _gameState: GameState, employeeId: str, attempt: int) -> GameState:
        gameState = _gameState.model_copy(deep=True)
        state_message = HumanMessage(content=f"Your name is : {employeeId}. \nCurrent game state:\n{gameState.to_prompt()}")
        
        employee = gameState.employees[employeeId]
        response = await self.llm.invoke_cached(employee.instruction, state_message, employee.get_messages())
        # Update the employee's messages with the response
        action = parse_tool(response.tool_name, response.tool_args)

        # This is a copy, do not try to mutate the original employee or game state
        result = performAction(gameState, employee, action)

        decision = AgentDecision(action=repr(action), 
                                 response=ResponseMessage(content=response.original_response.content),
                                 result=ToolResultMessage(tool=response.tool_name, tool_id= response.tool_id, tool_output=result.message, is_error=not result.success),
                                 invocation=ToolInvocationMessage(tool=response.tool_name, tool_input=response.tool_args, tool_id=response.tool_id),
                                 )
        newEmployee = result.game_state.grab_employee(employeeId)
        if attempt == 0:
            newEmployee.new_turn(decision)
        else:
            newEmployee.add_to_current_turn(decision)

        with open("responses1.txt", "a") as f:
            f.write(f"Turn: {gameState.tick}\n")
            f.write(f"Attempt: {attempt}\n")
            f.write(f"Employee: {employeeId}\n")
            f.write(f"Prompt: {response.prompt}\n")
            f.write(f"Response: {response.original_response.content}\n")
            f.write(f"Action: {repr(action)}\n")
            f.write(f"Result: {result.message}\n")
            f.write("\n")
        
        if result.success:
            # Update the game state with the result
            return result.game_state
        elif attempt < 3:
            # Retry the action
            return await self.process_recursive(result.game_state, employeeId, attempt + 1)
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
        case PickUpOrder():
            return pick_up_order(employee, gameState, toolResult)
        case _:
            raise Exception(f"Unknown tool: {toolResult}")