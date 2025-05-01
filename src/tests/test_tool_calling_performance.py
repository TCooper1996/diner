import pytest
from src.actions import create_tools, parse_tool
from src.actions.wait import WaitAction
from src.agents.employeeAgent import LLM
from src.agents.models import *
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage, SystemMessage

tools = create_tools()

@pytest.mark.asyncio
class TestToolCallingPerformance:
    def setup_method(self):
        """Setup method to initialize the model with tools"""
        self.model = LLM(ChatGPT(tools))

    @pytest.mark.asyncio
    async def test_1(self):
        name = "Alice"
        instruction = "You will seat customers in the restaurant as they arrive, and then take their orders."
        state_message = HumanMessage(content="Bob has taken an order from a customer. There are no customers waiting to be seated.")

        result = await self.model.invoke(name, instruction, state_message, [])
        action = parse_tool(result.tool_name, result.tool_args)
        assert action == WaitAction()