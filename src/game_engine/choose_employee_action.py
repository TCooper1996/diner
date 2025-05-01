
import copy
from dataclasses import dataclass
from itertools import chain
from typing import Any, Callable, List, Protocol, Tuple
from src.actions import Action, parse_tool
from src.agents.models.Model import Model, ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.common.results import  ValidationResult

from src.game_engine.shared_types import InvokeLLM, InvokeLLMWithMessages

ActionVerifier = Callable[[Action], ValidationResult]

@dataclass
class EmployeeAgentAttempt:
    """Represents an attempt made by the AI agent to perform an action, which may or may not have been valid."""
    selected_action: Action
    # These come from the agents response
    text_response: ResponseMessage
    tool_invocation: ToolInvocationMessage

ActionResultString = str
validation_successful = bool
@dataclass
class ChooseActionFromAgentUsecase:
    invoke_llm: InvokeLLM

        
    
    async def choose_next_action(self) ->   EmployeeAgentAttempt:
        #game_state_message = f"Your name is : {name}. \nCurrent game state:\n{r_state.to_prompt()}"
        #state_message = HumanMessage(content=agent_input.state_message)
        response = await self.invoke_llm()
        #response =  await llm.invoke_cached(agent_input.employee_instruction, state_message, agent_input.employee_messages)
        action = parse_tool(response.tool_name, response.tool_args)

        return EmployeeAgentAttempt(action,
                                    ResponseMessage(content=response.original_response.content),
                                    ToolInvocationMessage(tool=response.tool_name, tool_input=response.tool_args, tool_id=response.tool_id),
                                    )
                                    #ToolResultMessage(tool=response.tool_name, tool_id= response.tool_id, tool_output=action_result_string, is_error= not validation_success),