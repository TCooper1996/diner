import { Position } from "../common/Position";

export class PickupCounter {
    constructor(
        public readonly id: string,
        public readonly position: Position
    ) {}
}