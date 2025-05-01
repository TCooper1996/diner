from types import CoroutineType
from typing import Any, Callable, Coroutine, List

from src.agents.employeeAgent import LLMResult
from src.agents.models.Model import StandardMessage


InvokeLLM = Callable[[], Coroutine[Any, Any, LLMResult]]
InvokeLLMWithMessages = Callable[[List[StandardMessage]], Coroutine[Any, Any, LLMResult]]

StateMessage = str
InvokeLLMWithMessagesAndStateMessage = Callable[[StateMessage, List[StandardMessage]], CoroutineType[Any, Any, LLMResult]]