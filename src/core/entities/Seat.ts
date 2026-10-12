/**
 * Represents a seat in the restaurant.
 */
export class Seat {
    constructor(
        public readonly seatId: string,
        public readonly position: { x: number; y: number }
    ) {}
} 