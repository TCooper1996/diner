
import pytest
from src.actions import create_tools
from src.actions.move import MoveToNewRoom
from src.agents.RefinementAgent import RefinementAgent

@pytest.mark.asyncio
async def test_refinement():
    agent = RefinementAgent()
    response = await agent.refine_prompt("Alice seats customers as soon as they arrive, and if no seats are available, she waits patiently at the entrance.")
    print(response)
    assert 1 == 1