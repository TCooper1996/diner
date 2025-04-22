import asyncio
import base64
import copy
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

# Import actions from the new actions package
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
    game_state_prompt: str
    messages: List[str]

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

    async def invoke_cached(self, name, prompt, state_message, messages) -> LLMResult:
        # caching
        cache = {}
        if os.path.exists("responses.json"):
            with open("responses.json", "r") as f:
                d = f.read()
                cache = json.loads(d)  # Load existing cache
        key = str({"prompt": prompt, "state_message": state_message, "messages": [repr(m) for m in messages]})
        if key in cache:
            return pickle.loads(base64.b64decode(cache[key]))
        response = await self.invoke(name, prompt, state_message, messages)
        cache[key] = base64.b64encode(pickle.dumps(response)).decode('utf-8')
        with open("responses.json", "w") as f:
            json.dump(cache, f)
        return response

    async def invoke(self, name, prompt, state_message, _messages) -> LLMResult:
        
        system_message = SystemMessage(content=f"Instructions: {prompt}")
        messages = [*_messages]

        if len(messages) > 0:
            if messages[-1].is_error:
                messages.append(HumanMessage(content="Tool invocation failed: Your last action was invalid. Try again."))
            else:
                messages.append(HumanMessage(content="Tool invocation successful"))
        
        # Explicit query at the end
        human_message = HumanMessage(content=f"""
        Provide a breif summary of your next action based on the current state of the restaurant and your instructions and then respond with the tool invocation.
    """)

        i = -1
        while True:
            i += 1
            start = time.perf_counter()
            text, tool_call = await self.model.ainvoke([
                system_message,
                *messages,  # Limit to the last 5 messages for context
                state_message,
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
                prompt=prompt,
                game_state_prompt=state_message.content,
                messages=[repr(msg) for msg in messages] if messages else []
            )
            return result    
    