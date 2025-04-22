from dataclasses import dataclass
from typing import List

from src.common.position import Position
from src.core.entities.info import CustomerInfo, StationInfo
from . import RestaurantState
from .entities import Employee

    
@dataclass
class EmployeeInfo:
    e: Employee
    position: Position

    @property
    def name(self) -> str:
        return self.e.name
    

class RestaurantViewer:
    @classmethod
    def view_employees(cls, state: RestaurantState) -> List[EmployeeInfo]:
        return [EmployeeInfo(e, state.get_position_of(e.name)) for e in state.employees.values()]

    @classmethod
    def view_stations(cls, state: RestaurantState) -> List[StationInfo]:
        return [StationInfo(s.station_id, state.get_position_of(s.station_id), s.station_type) for s in state.station_manager.get_stations()]

    @classmethod
    def view_customers(cls, state: RestaurantState) -> List[CustomerInfo]:
        return list(CustomerInfo(c.name, c.status, c.eating_time, state.get_position_of(c.id)) for c in state.customers.values())