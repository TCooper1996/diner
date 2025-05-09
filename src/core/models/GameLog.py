from typing import Literal, Protocol

LogType = Literal["agent_response", "action_failed", "action_success", "misc"]
class GameLog(Protocol):
    def get_log(self) -> str:
        ...
    def get_log_turn(self) -> int:
        ...
    def get_log_type(self) -> LogType:
        ...