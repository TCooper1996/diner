from dataclasses import dataclass
from typing import Optional, TypeVar



@dataclass
class ActionResult:
    message: str
    repeat: bool = False

@dataclass
class ValidationResult:
    success: bool
    error_msg: Optional[str] = None
