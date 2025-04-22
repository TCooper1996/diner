from .employee_info import EmployeeInfo
from .customer_info import CustomerInfo
from .station_info import StationInfo
from .floor_info import FloorInfo

EntityInfo = EmployeeInfo | CustomerInfo | StationInfo | FloorInfo

all__ = [
    "EntityInfo",
    "EmployeeInfo",
    "CustomerInfo",
    "StationInfo",
    "FloorInfo"
]