import time
from typing import Dict, List, Annotated, TypedDict, Callable, Any, Optional, Tuple
import os
import json

from dotenv import load_dotenv
from langchain import hub
from langchain.prompts import PromptTemplate, MessagesPlaceholder
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.agents import AgentAction, AgentFinish
import langgraph.graph as lg
from pydantic import BaseModel, Field

from src.state.employee import Employee
from src.state.game import GameState
from src.game_engine.location import Location
from src.tools.restaurant_tools import (
    ActionResult,
    move_to_location,
    notify_kitchen_of_orders,
    seat_customer,
    take_order,
    cook_food,
    deliver_food,
    observe_environment
)
from src.utils.env import get_anthropic_api_key
from src.agents.employee_tools import *


# State that flows through the graph during execution
class AgentGraphState(BaseModel):
    # References to persistent state
    employee_state: Employee
    game_state: GameState
    

# Employee controller class that processes employee actions
class EmployeeAgentController:
    def __init__(self): 
        self.model = "chatgpt"
        # Setup the LLM
        load_dotenv()
        chatgpt="gpt-4o-mini-2024-07-18"
        claude = "claude-3-5-haiku-latest"
        llm = ChatAnthropic(
            model=claude,
            temperature=0,
            anthropic_api_key=get_anthropic_api_key()
        )

        self.llm = llm.bind_tools(create_tools())


    def process(self, gameState: GameState, employeeId: str) -> Tuple[EmployeeAction, GameState]:
        employee = gameState.employees[employeeId]
        # Construct prompt for planning
        planning_template = """
        You are {name}, an employee at a diner. Your instructions are: '{instruction}'

        Only perform duties relevant to your instructions.

        Here is some additional information that MAY OR MAY NOT be relavant to your role:
        Subject: Orders
        - Orders are created when athe 'TakeOrder' tool is used in the dining area where there are customers who haven't ordered yet.
        - A newly created order is in the 'pending' state.
        - Orders are moved to the 'TAKEN' state when the 'NotifyKitchenOfOrders' tool is used in the kitchen.
        - Orders are moved to the 'COOKING' state when the 'Cook' tool is used in the kitchen.
        - Orders are moved to the 'READY' state when they are ready to be delivered to the customer.
        - Orders are moved to the 'DELIVERED' state when they are delivered to the customer
        - Orders move strictly in the following order: pending -> taken -> cooking -> ready -> delivered
        - Orders can only be delivered when the DeliverTool is used in the DINING ROOM.
        - Orders cannot be delivered if the employee is not in the DINING ROOM.
        - An employee must move to the dining room to deliver food to customers.

        
        Based on your instructions and the current state of the restaurant,
        decide what you should do next.

        Here is the current state of the restaurant:
        {observation}            
        End of restaurant state.


        Here are some of your recent thoughts:
        {recent_thoughts}

        
        Respond with no more than a single sentence describing your intention and then
        choose the action you think is best based on your instructions.
        """
        
        planning_prompt = PromptTemplate.from_template(planning_template)
        
        # Get all messages from the employee's history
        #chat_history = "\n".join([msg.content for msg in state.employee_state.messages[-10:]])

        observation = observe_environment(employee, gameState)

        # Personal state
        #ordersOwned = [o for o in gameState.orders.values() if o.server == employeeId]
        #if ordersOwned:
        #    observation += f"\nYou have {len(ordersOwned)} orders that must be brought to the kitchen."

        recent_thoughts = employee.recentThoughts[-10:]
        
        planning_input = planning_prompt.format(
            name=employee.name,
            recent_thoughts=recent_thoughts,
            instruction=employee.instruction,
            observation=observation,
        )
        
        # Add the planning query to employee's messages
        planning_message = HumanMessage(content=planning_input)
       

        # Get a response from the LLM
        startTime = time.perf_counter()
        response = self.llm.invoke([*recent_thoughts, planning_message])
        endTime = time.perf_counter()
        print(f"Planning took {endTime - startTime} seconds")
        selectedTool = None
        selectedTool = response.content[1]
        # Update the employee's messages with the response
        toolResult = parse_tool(selectedTool["name"], selectedTool["input"])
        employee.action = toolResult
        # Does the response need to be saved to memory?
        employee.add_thought(response)

        result = None
        match (toolResult):
            case MoveTool(destination=destination):
                result  = move_to_location(employee, gameState, destination)
            case SeatTool():
                result  = seat_customer(employee, gameState)
            case TakeOrderTool():
                result  = take_order(employee, gameState)
            case CookTool(order_id=order_id):
                result  = cook_food(employee, gameState, order_id)
            case DeliverTool():
                result  = deliver_food(employee, gameState)
            case WaitTool():
                result  = ActionResult(True, "Waiting for next instruction", gameState)
            case NotifyKitchenOfOrdersTool():
                result  = notify_kitchen_of_orders(employee, gameState)
            case _:
                raise Exception(f"Unknown tool: {toolResult}")

        employee.add_thought(ToolMessage(content=result.message, type="tool", tool_call_id=selectedTool["id"]))
        return employee.action, result.game_state

