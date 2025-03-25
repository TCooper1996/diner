import json
import pytest
from src.actions import create_tools, parse_tool
from src.actions.cook import CookAction
from src.actions.move import MoveToNewRoom
from src.actions.seat import SeatAction
from src.actions.wait import WaitAction
from src.agents.RefinementAgent import RefinementAgent
from src.agents.models.Claude import Claude
from src.agents.models.Llama import Llama
from langchain_core.messages import SystemMessage, HumanMessage


#llm = Llama("qwen2.5:32b", create_tools())
llm = Claude(create_tools())
current_state = {"customersWaitedToBeSeated": ["herbert"], "pendingOrders": 2}
command_message = """
- if pendingOrders < 5: Invoke SeatAction. 
- Otherwise, if pendingOrders > 5: invoke MoveToNewRoom(destination=kitchen)
You must choose 1 tool
"""
@pytest.mark.asyncio
async def test_seat_customer():
    command = HumanMessage(content=command_message)
    state_message = json.dumps(current_state)
    messages = [HumanMessage(content=state_message), command]

    response = await llm.ainvoke(messages)
    action = parse_tool(response[1].tool, response[1].tool_input)
    assert action == SeatAction(customer_id="herbert")
    print()

@pytest.mark.asyncio
async def test_move():
    command = HumanMessage(content=command_message)
    new_state = {**current_state}
    new_state["pendingOrders"] = 7
    state_message = json.dumps(new_state)
    messages = [HumanMessage(content=state_message), command]

    response = await llm.ainvoke(messages)
    action = parse_tool(response[1].tool, response[1].tool_input)
    assert action == MoveToNewRoom(destination="kitchen")

@pytest.mark.asyncio
async def test_nested_decision():
    command = HumanMessage(content="If there are more than 5 unseated customers, invoke SeatAction on one of them. Otherwise invoke Wait()")
    new_state = {"unseatedCustomers": ["herbert", "john", "jane", "jill", "jack", "jill"]}
    state_message = json.dumps(new_state)
    messages = [HumanMessage(content=state_message), command]

    response = await llm.ainvoke(messages)
    action = parse_tool(response[1].tool, response[1].tool_input)
    assert isinstance(action, SeatAction)

    new_state = {"unseatedCustomers": ["herbert", "john", "jane", "jill"]}
    state_message = json.dumps(new_state)
    messages = [HumanMessage(content=state_message), command]

    response = await llm.ainvoke(messages)
    action = parse_tool(response[1].tool, response[1].tool_input)
    assert isinstance(action, WaitAction)
