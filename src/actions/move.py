"""Move action implementation"""

from typing import ClassVar, List, Literal, Optional
from pydantic import BaseModel, Field

from src.core.models.Action import ActionResult, ValidationResult
from src.core.types import StationType, Stations
from src.core.models.RestaurantState import RestaurantState


class MoveToNewRoom(BaseModel):
    """
    Tool for moving an employee to a different location
    """
    destination: StationType = Field(
        description=f"The location to move to. Options are {Stations}"
    )

    def is_valid(self, state: RestaurantState, employee_id: str) -> ValidationResult:
        current_location = get_current_location(state, employee_id)
        
        if current_location == self.destination:
            return ValidationResult(False, f"{employee_id} is already at the {self.destination}.")
        
        if self.destination.lower() not in Stations:
            return ValidationResult(False, f"Cannot move to {self.destination}. Valid locations are: {', '.join(Stations)}")
        
        return ValidationResult(True, None)

    def execute(self, state: RestaurantState, employee_id: str) -> ActionResult:
        current_location = get_current_location(state, employee_id)
        station_id = find_station(state, self.destination)
        
        if station_id:
            # Lock the station
            lock_station(state, station_id, employee_id)
            
            # Move employee toward the station
            repeat = not approach_entity(state, employee_id, station_id)
            new_location = get_current_location(state, employee_id)
            
            return ActionResult(f"{employee_id} moved from {current_location} to {new_location}", repeat=repeat)
        else:
            return ActionResult(f"Could not find a {self.destination} station to move to.", repeat=False)


# Utilities --------------------------------
def get_current_location(state: RestaurantState, employee_id: str) -> str:
    """Get the current location type of the employee."""
    employee = state.get_employee_repo().get_employee(employee_id)
    # This would need to be implemented to determine location based on position
    # For now just return a placeholder
    position = employee.position
    # This is a simplified version - in a real implementation you'd use a service 
    # to determine the type of location the employee is in
    return "unknown"  # Placeholder implementation

def find_station(state: RestaurantState, station_type: str) -> Optional[str]:
    """Find a station of the given type."""
    # This is a simplified implementation - you would need to query the appropriate repo
    # For now just return a placeholder station ID
    return f"{station_type}-1"  # Placeholder implementation

def lock_station(state: RestaurantState, station_id: str, employee_id: str):
    """Lock a station for an employee's use."""
    # In a real implementation, this would update a repository to mark the station as in use
    pass  # Placeholder implementation

def approach_entity(state: RestaurantState, employee_id: str, entity_id: str) -> bool:
    """Move employee toward an entity and return True if reached."""
    employee = state.get_employee_repo().get_employee(employee_id)
    
    # This is a simplified implementation - in a real system you'd get the entity position
    # from the appropriate repository based on the entity ID and type
    entity_position = None  # You would get this from the appropriate repository
    
    # For now, just simulate movement
    # If we had the entity position, we would:
    # 1. Get path between employee and entity
    # 2. Move employee along path
    # 3. Check if employee has reached entity
    
    # Placeholder: always return False to indicate not yet reached
    return False
