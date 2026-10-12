/**
 * Represents a grill in the restaurant.
 */
export class Grill {
    constructor(
        public readonly grillId: string,
        public readonly position: { x: number; y: number }
    ) {}
} 