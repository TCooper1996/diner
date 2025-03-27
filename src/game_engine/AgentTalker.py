from dataclasses import dataclass
from typing import List

from src.agents.employeeAgent import LLM, LLMResult
from src.agents.models.Model import StandardMessage


@dataclass
class AgentTalker:
    llm: LLM
    messages: List[StandardMessage]

    async def invoke(self, prompt: str, state_message: str) -> LLMResult:
        return await self.llm.invoke(prompt, state_message, self.messages)
