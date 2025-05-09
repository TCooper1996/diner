from src.common.position import Position
from src.core.services.NavigationService import NavigationService
from src.infrastructure.navigation.floor_plan import FloorPlan


class NavigationServiceImpl(NavigationService):
    def __init__(self, floor_plan: FloorPlan):
        self.floor_plan = floor_plan

    def get_path_between_positions(self, start: Position, end: Position) -> list[Position]:
        return self.floor_plan.find_path(start, [end])

    def move_toward(self, start: Position, end: Position) -> Position:
        return self.get_path_between_positions(start, end)[1]

    def get_closest_entity(self, has_position: Position, entities: list[Position]) -> int:
        closest_entity_index = -1
        closest_distance = float("inf")
        for i, entity in enumerate(entities):
            distance = len(self.get_path_between_positions(has_position, entity)) - 1
            if distance < closest_distance:
                closest_distance = distance
                closest_entity_index = i
        return closest_entity_index
