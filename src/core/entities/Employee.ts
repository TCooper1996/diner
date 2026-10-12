/**
 * Represents an employee in the restaurant.
 */
export class Employee {
    constructor(
        public readonly name: string,
        public readonly position: { x: number; y: number }
    ) {}
} 