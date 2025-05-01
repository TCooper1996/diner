import datetime
from typing import List, Optional, Tuple, Union
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from src.agents.models.Model import Model, ResponseMessage, StandardMessage, StandardToOpenAIMessages, ToolInvocationMessage, ToolResultMessage
from src.utils.env import get_anthropic_api_key
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage, SystemMessage


class Claude(Model):
    def __init__(self, tools: List):
        load_dotenv()
        claude = "claude-3-5-haiku-latest"
        # type: ignore
        self.llm = ChatAnthropic(
            model=claude,
            temperature=0,
            anthropic_api_key=get_anthropic_api_key(),
        ).bind_tools(tools, tool_choice="auto")

    async def ainvoke(self, _messages: List[StandardMessage]) -> Tuple[ResponseMessage, Optional[ToolInvocationMessage]]:
        messages = StandardToOpenAIMessages(_messages)
        response = await self.llm.ainvoke(messages)



        responseText = ResponseMessage(content="")
        toolResponse = None

        if not isinstance(response.content, list):
            responseText = ResponseMessage(content=response.content)
            return responseText, toolResponse

        for item in response.content:
            if item["type"] == "tool_use":
                toolResponse = ToolInvocationMessage(
                    tool=item["name"],
                    tool_input=item["input"],
                    tool_id=item["id"]
                )
            if item["type"] == "text":
                responseText = ResponseMessage(content=item["text"])

        return responseText, toolResponse