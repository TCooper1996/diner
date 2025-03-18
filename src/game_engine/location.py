from enum import Enum
from typing import Literal

ENTRANCE: Literal["entrance"] = "entrance"
DINING: Literal["dining"] = "dining"
KITCHEN:  Literal["kitchen"] = "kitchen"
GONE:  Literal["gone"]  = "gone"
Location = Literal["entrance", "dining", "kitchen", "gone"]
