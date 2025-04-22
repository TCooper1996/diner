import json
import os
from typing import Dict, List, Optional, Tuple, Type, Union
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from openai import OpenAI
from pydantic import BaseModel  # Ensure you have the correct import for ChatGPT

from src.agents.models.Model import Model, ResponseMessage, StandardMessage, StandardToOpenAIMessages, ToolInvocationMessage, ToolResultMessage
from src.protocols import IAction
from src.utils.env import get_anthropic_api_key
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage, SystemMessage


class GPT(Model):
    def __init__(self, tools: List):
        self.tools = [self.to_tool_schema(tool) for tool in tools]
        load_dotenv()
        claude = "gpt-4o"
        # type: ignore
        load_dotenv()
        self.client = OpenAI()

    def to_tool_schema(self, action: Type[BaseModel]):
        schema = action.model_json_schema()
        return {
            "type": "function",
            "function": {
                "name": action.__name__,
                "description": action.__doc__.strip(),
                "parameters": {
                    "type": "object",
                    "properties": schema.get("properties", {}),
                    "required": schema.get("required", []),
                    "additionalProperties": False  # Ensure no extra properties are allowed
                },
                "strict": True
            }
        }

    async def ainvoke(self, _messages: List[StandardMessage]) -> Tuple[ResponseMessage, Optional[ToolInvocationMessage]]:
        messages = self.to_messages(_messages)

        response = self.client.chat.completions.create(model="o1", messages=messages, tools=self.tools)

        if response.choices[0].message.tool_calls is None:
            return ResponseMessage(content=""), None


        f = response.choices[0].message.tool_calls[0].function
        toolResponse = ToolInvocationMessage(
            tool=f.name,
            tool_input=json.loads(f.arguments),
            tool_id=""
        )
        content = response.choices[0].message.content
        responseText = ResponseMessage(content=content if content else "")

        return responseText, toolResponse

    def to_messages(self, _messages: List[StandardMessage]) -> List[Dict[str, any]]:
        messages = []
        for m in _messages:
            messages.append(to_message(m))
        return messages

def to_message(m: StandardMessage):
    match m:
        case SystemMessage():
            return {"role": "system", "content": m.content}
        case HumanMessage():
            return {"role": "user", "content": m.content}
        case ResponseMessage():
            return {"role": "assistant", "content": m.content}
        case ToolResultMessage():
            return {"role": "function", "name": m.tool, "content": m.tool_output}
        case ToolInvocationMessage():
            return {"role":"assistant", "content": "null", "function_call": {
                "name": m.tool,
                "arguments": str(m.tool_input)
            }}
