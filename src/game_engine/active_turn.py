
from dataclasses import dataclass


@dataclass
class EmployeeUpdate:
    index: int

class CustomerUpdate:
    pass

ActiveTurn = EmployeeUpdate | CustomerUpdate