from typing import Literal, Protocol



class ChooseActionGameLog(Protocol):
    def get_action_name(self) -> str:
        ...
    def get_action_args(self) -> str:
        ...
    def get_response(self) -> str:
        ...
    def get_result(self) -> str:
        ...
    def was_successful(self) -> bool:
        ...

class ContinueActionGameLog(Protocol):
    def get_desc(self) -> str:
        ...



LogType = ContinueActionGameLog | ChooseActionGameLog
class GameLog(Protocol):
    def get_log(self) -> str:
        ...
    def get_log_turn(self) -> int:
        ...
    def get_log_type(self) -> LogType:
        ...