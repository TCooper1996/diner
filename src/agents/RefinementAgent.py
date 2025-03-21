import json
from typing import Type
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from src.actions import create_tools
from src.utils.load_readme import load_readme


refinement_prompt = """
# 🍽️ Diner Simulation Game (Instruction Refinement)

Below is the detailed documentation of our restaurant management game. You will receive **player-written instructions for AI-powered employees**. Your job is to refine these natural-language instructions into a clear, structured format.

# 📖 Game Documentation
{README_CONTENT}

# 🛠️ Available Tools
{DYNAMICALLY_GENERATED_TOOL_LIST}

---

## 📝 Task:
Given the player's prompt, generate a structured instruction for the AI employee, including:

- **Role:** Clearly identify the employee's primary responsibility based on the prompt.
- **Tasks:** Break down the player's instruction into specific, well-defined tasks.
- **Allowed Actions:** Suggest appropriate tools based on the described tasks.
- **Forbidden Actions:** Explicitly list actions unrelated or prohibited based on the player's instruction.
- **Edge Cases:** Briefly state how the employee should handle common edge cases (e.g., "if no customers are waiting, remain idle").

**Example:**

### Player Prompt:
"Alice seats customers as soon as they arrive, and if no seats are available, she waits patiently at the entrance."

### Structured Employee Instruction:
```json
{{{{
  "role": "Hostess",
  "tasks": ["Seat customers immediately upon arrival."],
  "allowed_actions": ["SeatCustomer", "Wait"],
  "forbidden_actions": ["CookOrder", "ServeOrder", "CleanTable", "TakeOrder"],
  "edge_cases": "If no seats are available, remain idle at the entrance."
}}}}
```

Now, perform the refinement for the following prompt:

Player Prompt:

"{{PLAYER_PROMPT}}"

Structured Employee Instruction:
"""

def tool_schema_description(tool_cls: Type[BaseModel]) -> str:
    fields = tool_cls.model_fields
    field_descriptions = "\n".join(
        f"- **{name}** (`{field.annotation.__name__}`): {field.description or 'No description.'}"
        for name, field in fields.items()
    )
    return f"""
### {tool_cls.__name__}
{tool_cls.__doc__ or "No description provided."}

**Fields:**
{field_descriptions}
"""

def cache_refinement(fn):
    cache = {}
    async def wrapper(self, client_prompt):
        nonlocal cache
        with open("cache.json", "r") as f:
            cache = json.load(f)

        if client_prompt in cache:
            return cache[client_prompt]
        result = await fn(self, client_prompt)
        cache[client_prompt] = result
        with open("cache.json", "w") as f:
            json.dump(cache, f)
        return result
    return wrapper
class RefinementAgent:
    def __init__(self):
        #self.llm = ChatAnthropic(model="claude-3-5-haiku-latest", temperature=0)
        self.llm = ChatOllama(model="gemma:2b", temperature=0)
        background = load_readme()
        tool_info = "\n".join(tool_schema_description(tool) for tool in create_tools())
        self.partial_prompt = refinement_prompt.format(
            README_CONTENT=background, 
            DYNAMICALLY_GENERATED_TOOL_LIST=tool_info)

    async def invoke(self, client_prompt, tools=None) -> str:
        # Get a response from the LLM
        if tools:
            llm = self.llm.bind_tools(tools)
            return await llm.ainvoke([HumanMessage(client_prompt)])
        return await self.llm.ainvoke(client_prompt)

    @cache_refinement
    async def refine_prompt(self, client_prompt) -> str:
        # Get a response from the LLM
        prompt = self.partial_prompt.format(PLAYER_PROMPT=client_prompt)

        response = await self.llm.ainvoke(prompt)
        return response.content
    