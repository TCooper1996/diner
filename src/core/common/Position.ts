export interface Position {
    x: number;
    y: number;
}

export function newPosition(x: number, y: number): Position {
    return { x, y };
}

export function positions_are_equal(pos1: Position, pos2: Position): boolean {
    return pos1.x === pos2.x && pos1.y === pos2.y;
}