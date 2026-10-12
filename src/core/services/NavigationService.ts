import { Position } from '@core/common/Position';

export interface NavigationService {
    /**
     * Get the path between two positions. Includes the start and end positions
     */
    getPathBetweenPositions(start: Position, end: Position): Position[];

    /**
     * Get the next position in the path between two positions. Includes the start and end positions
     */
    moveToward(start: Position, end: Position): Position;

    /**
     * Returns the index of the closest entity in the list
     */
    getClosestEntity(hasPosition: Position, entities: Position[]): number;

    /**
     * Returns the floor plan of the restaurant
     */
    getFloorPlan(): Position[];
} 