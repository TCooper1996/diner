from typing import List, Optional, Tuple
from langchain_ollama import ChatOllama
from src.agents.models.Model import Model, ResponseMessage, StandardMessage, StandardToOpenAIMessages, ToolInvocationMessage


class Llama(Model):
    
    def __init__(self, name: str, tools: List[str]):
        self.llm = ChatOllama(
            model=name,
            temperature=0
        ).bind_tools(tools, tool_choice="auto")

    async def ainvoke(self, _messages: List[StandardMessage]) -> Tuple[ResponseMessage, Optional[ToolInvocationMessage]]:
        messages = StandardToOpenAIMessages(_messages)

        response = await self.llm.ainvoke(messages)


        responseText = ResponseMessage(content=response.content)
        tool = response.tool_calls[0]
        toolResponse = ToolInvocationMessage(tool=tool["name"], tool_input=tool["args"], tool_id=tool["id"])

        return responseText, toolResponse