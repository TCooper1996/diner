from typing import Dict, List, Literal, Optional, Tuple, Union
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage, SystemMessage

from pydantic import BaseModel




class ResponseMessage(BaseModel):
    content: str

class ToolInvocationMessage(BaseModel):
    tool: str
    tool_input: Dict[str, str]
    tool_id: str

class ToolResultMessage(BaseModel):
    tool: str
    tool_output: str
    tool_id: str
    is_error: bool


StandardMessage = Union[ResponseMessage, ToolInvocationMessage, ToolResultMessage, HumanMessage, SystemMessage]

class Model:
    async def ainvoke(self, messages: List[StandardMessage]) -> Tuple[ResponseMessage, Optional[ToolInvocationMessage]]:
        raise NotImplementedError

def StandardToOpenAIMessages(_messages: List[StandardMessage]) -> List[BaseMessage]:
    messages: List[BaseMessage] = []
    for m in _messages:
        match (m):
            case ResponseMessage():
                messages.append(AIMessage(content = [{"type":"text", "text": m.content}]))
            case ToolInvocationMessage():
                messages[-1].content.append({"type": "tool_use", "name": m.tool, "input": m.tool_input, "id": m.tool_id})
            case ToolResultMessage():
                messages.append(HumanMessage(content = [{"type": "tool_result",  "content": m.tool_output, "tool_use_id": m.tool_id, "is_error": m.is_error}]))
            case HumanMessage():
                messages.append(m)
            case SystemMessage():
                messages.append(m)
            case _:
                raise Exception("Unknown message type")
    return messages