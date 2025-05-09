
from dataclasses import dataclass


@dataclass
class EmployeeUpdate:
    index: str

class CustomerUpdate:
    pass

ActiveTurn = EmployeeUpdate | CustomerUpdate